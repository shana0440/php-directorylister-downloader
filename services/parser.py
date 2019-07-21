from typing import List, Callable
from urllib.parse import (
  urlparse,
  parse_qs,
  unquote,
)

from bs4 import BeautifulSoup
import requests

from models.link import Link

class Parser():
  on_folder_updated_observers: Callable[[Link, str], None] = []

  def get_folder_tree(self, entry_point: str) -> Link:
    root_link = Link(
      url=entry_point,
      path=self.get_current_folder(entry_point),
      name=self.get_current_folder(entry_point),
      is_folder=True,
      children=[]
    )
    stack = [root_link]
    while stack:
      link = stack.pop()
      if link.is_folder:
        links = self.list_children(link)
        link.children = links
        [self.notify_folder_updated(link) for link in links]
        [stack.append(link) for link in links]

    return root_link

  def list_children(self, link: Link) -> List[Link]:
    parsed_url = urlparse(link.url)
    url_prefix = "%s://%s%s" % (parsed_url.scheme, parsed_url.hostname, parsed_url.path)
    resp = requests.get(link.url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = soup.find_all('a', class_="clearfix")
    # Remove back to parent link
    links = list(filter(lambda x: x.get('data-name').strip() != '..', links))
    return list(map(lambda x: Link(
      name=x.get('data-name').strip(),
      path="%s/%s" % (link.path, x.get('data-name').strip()),
      url=url_prefix + x.get('href'),
      is_folder=self.is_folder(x.get('href')),
      children=[]
    ), links))

  def is_folder(self, url: str) -> bool:
    return url.startswith('?dir=')

  def get_current_folder(self, url: str) -> str:
    parsed_url = urlparse(url)
    qs = parse_qs(parsed_url.query)
    paths = qs['dir'].pop().split("/")
    current_folder = paths.pop()
    return unquote(current_folder)

  def on_folder_updated(self, observer: Callable[[Link, str], None]):
    self.on_folder_updated_observers.append(observer)

  def notify_folder_updated(self, link: Link):
    [observer(link) for observer in self.on_folder_updated_observers]
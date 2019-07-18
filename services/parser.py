from typing import List
from urllib.parse import (
  urlparse,
  parse_qs,
  unquote,
)

from bs4 import BeautifulSoup
import requests

from models.link import Link

class Parser():
  def run(self, entry_point: str) -> List[Link]:
    files = self.list(entry_point)
    for file in files:
      if file.is_folder:
        file.children = self.run(file.url)
    return files

  def list(self, url: str) -> List[Link]:
    parsed_url = urlparse(url)
    url_prefix = "%s://%s%s" % (parsed_url.scheme, parsed_url.hostname, parsed_url.path)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = soup.find_all('a', class_="clearfix")
    # Remove back to parent link
    links = list(filter(lambda x: x.get('data-name').strip() != '..', links))
    return list(map(lambda x: Link(
      name=x.get('data-name').strip(),
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
    return current_folder

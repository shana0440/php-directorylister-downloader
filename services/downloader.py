import os
from typing import List

import requests

from models.link import Link

class Downloader():
  def download(self, link: Link, to: str):
    with requests.get(link.url, stream=True) as resp:
      with open("%s/%s" % (to, link.name), 'wb') as file:
        for chunk in resp.iter_content(chunk_size=5120):
          if chunk: file.write(chunk)

  def download_links(self, links: List[Link], to: str):
    for link in links:
      if link.is_folder:
        folder = "%s/%s" % (to, link.name)
        if not os.path.exists(folder):
          os.mkdir(folder)
        self.download_links(link.children, folder)
      else:
        self.download(link, to)
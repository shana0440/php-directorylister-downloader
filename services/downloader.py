import os
import sys
from typing import List

import requests

from models.link import Link

class Downloader():
  def download(self, link: Link, to: str):
    with requests.get(link.url, stream=True) as resp:
      total_length = int(resp.headers.get('content-length'))
      filename = "%s/%s" % (to, link.name)
      with open(filename, 'wb') as file:
        current_progress = 0
        for chunk in resp.iter_content(chunk_size=5120):
          if chunk:
            current_progress += len(chunk)
            file.write(chunk)
            self.print_progress(current_progress, total_length, filename)
      print()

  def print_progress(self, current: int, total: int, filename: str):
    done = int(50 * current / total)
    sys.stdout.write("\r[%s%s] %s" % ('=' * done, ' ' * (50 - done), filename))
    sys.stdout.flush()

  def download_links(self, links: List[Link], to: str):
    for link in links:
      if link.is_folder:
        folder = "%s/%s" % (to, link.name)
        if not os.path.exists(folder):
          os.mkdir(folder)
        self.download_links(link.children, folder)
      else:
        self.download(link, to)
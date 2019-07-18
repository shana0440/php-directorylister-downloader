import os
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import List

import requests

from models.link import Link

class Downloader():
  def download(self, link: Link, to: str):
    with requests.get(link.url, stream=True) as resp:
      total_length = int(resp.headers.get('content-length'))
      filename = "%s/%s" % (to, link.path)
      with open(filename, 'wb') as file:
        current_progress = 0
        for chunk in resp.iter_content(chunk_size=5120):
          if chunk:
            current_progress += len(chunk)
            file.write(chunk)
            self.print_progress(current_progress, total_length, filename)
      # break link
      print()

  def print_progress(self, current: int, total: int, filename: str):
    done = int(50 * current / total)
    sys.stdout.write("\r[%s%s] %s" % ('=' * done, ' ' * (50 - done), filename))
    sys.stdout.flush()

  def download_folder_tree(self, link: Link, to: str, executor: ThreadPoolExecutor):
    stack = [link]
    while stack:
      link = stack.pop()
      if link.is_folder:
        folder = "%s/%s" % (to, link.path)
        if not os.path.exists(folder):
          os.mkdir(folder)
        stack.extend(link.children)
      else:
        executor.submit(self.download, link, to)

  def download_folder_tree_async(self, link: Link, to: str, workers: int):
    with ThreadPoolExecutor(max_workers=workers) as executor:
      self.download_folder_tree(link, to, executor)

import os
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import List

import requests

from models.link import Link

class Downloader():
  executor: ThreadPoolExecutor

  def __init__(self, workers):
    self.executor = ThreadPoolExecutor(max_workers=workers)

  def __del__(self):
    self.executor.shutdown()

  def download(self, link: Link, to: str):
    if not link.is_folder:
      self.executor.submit(self._download, link, to)

  def _download(self, link: Link, to: str):
    self.make_folder(link, to)
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

  def make_folder(self, link: Link, to: str):
    folder_paths = link.path.split("/") if link.is_folder else os.path.dirname(link.path).split("/")
    for path in folder_paths:
      folder = "%s/%s" % (to, path)
      if not os.path.exists(folder):
        os.mkdir(folder)

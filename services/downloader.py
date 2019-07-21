import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Callable

import requests

from models.link import Link

class Downloader():
  executor: ThreadPoolExecutor
  on_download_progress_updated_observers: List[Callable[[int, int, str], None]] = []

  def __init__(self, workers: int):
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
          self.notify_current_progress_updated(current_progress, total_length, link.path)

  def make_folder(self, link: Link, to: str):
    folder_paths = link.path.split("/") if link.is_folder else os.path.dirname(link.path).split("/")
    folder = to
    for path in folder_paths:
      folder = "%s/%s" % (folder, path)
      if not os.path.exists(folder):
        os.mkdir(folder)

  def on_download_progress_updated(self, observer: Callable[[int, int, str], None]):
    self.on_download_progress_updated_observers.append(observer)

  def notify_current_progress_updated(self, current: int, total: int, filename: str):
    for observer in self.on_download_progress_updated_observers:
      observer(current, total, filename)
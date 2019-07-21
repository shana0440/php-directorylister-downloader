from collections import OrderedDict
import threading

from blessed import Terminal

class Printer():
  term = Terminal
  locations = OrderedDict()
  lock = threading.Lock()
  last_location = (0, 4)

  def __init__(self):
    self.term = Terminal()

  def print_progress(self, current: int, total: int, filename: str):
    self._print_progress(current, total, filename)

  def _print_progress(self, current: int, total: int, filename: str):
    with self.lock:
      done = int(50 * current / total)
      location = self.get_location(filename)
      with self.term.location(*location):
        print("[%s%s] %s" % ('=' * done, ' ' * (50 - done), filename))
    if current >= total:
      self.locations.pop(filename)

  def get_location(self, filename: str) -> (int, int):
    if filename in self.locations:
      return self.locations[filename]

    location = self.last_location
    self.last_location = (0, self.last_location[1] + 1)

    self.locations[filename] = location
    return self.locations[filename]

  def completed(self, filename: str):
    self._print_progress(1, 1, filename)
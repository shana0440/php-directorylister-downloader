import sys

class Printer():
  def print_progress(self, current: int, total: int, filename: str):
    done = int(50 * current / total)
    sys.stdout.write("\r[%s%s] %s" % ('=' * done, ' ' * (50 - done), filename))
    sys.stdout.flush()

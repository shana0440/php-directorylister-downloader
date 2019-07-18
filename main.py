from typing import List

from services.parser import Parser
from models.link import Link

def print_files(files: List[Link], indent: int = 0):
  for file in files:
    print("  " * indent + file.name)
    if file.is_folder:
      print_files(file.children, indent + 1)

parser = Parser()
files = parser.run('http://demo.directorylister.com/?dir=images/photos')
print_files(files)
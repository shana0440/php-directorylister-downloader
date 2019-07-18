import os
from typing import List

from services.parser import Parser
from services.downloader import Downloader
from models.link import Link

def print_links(links: List[Link], indent: int = 0):
  for link in links:
    print("  " * indent + link.name)
    if link.is_folder:
      print_links(link.children, indent + 1)

parser = Parser()
links = parser.run('http://demo.directorylister.com/?dir=images/photos')
print_links(links)
downloader = Downloader()
downloader.download_links(links, os.getcwd())

import os
from typing import List
import argparse

from services.parser import Parser
from services.downloader import Downloader
from models.link import Link

args_parser = argparse.ArgumentParser()
args_parser.add_argument("url", help="the dictinoary url you want to download")
args_parser.add_argument("--output", help="output to specific path, default is current path", default=os.getcwd())
args_parser.add_argument("--workers", help="the number used to download multiple files at sametime, default is 5", default=5)
args = args_parser.parse_args()

php_directory_lister_parser = Parser()
downloader = Downloader(args.workers)

php_directory_lister_parser.on_folder_updated(
  lambda link: downloader.download(link, args.output)
)

root = php_directory_lister_parser.get_folder_tree(args.url)

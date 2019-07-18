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

php_dictinoary_lister_parser = Parser()
links = php_dictinoary_lister_parser.run(args.url)
downloader = Downloader()
downloader.download_links_async(links, args.output, args.workers)

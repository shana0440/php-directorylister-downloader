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
args_parser.add_argument("--without-entry-folder", help="will directly download files into ouput folder without entry folder", default=False)
args = args_parser.parse_args()

php_directory_lister_parser = Parser()
links = php_directory_lister_parser.run(args.url)
current_folder = php_directory_lister_parser.get_current_folder(args.url)
downloader = Downloader()
output = "%s/%s" % (args.output, current_folder) if not args.without_entry_folder else args.output
downloader.download_links_async(links, output, args.workers)

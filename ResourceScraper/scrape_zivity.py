import logging
import argparse
import os
import sys

from scrape import Scrape
from zivity import ZivityScraper

root_log = logging.getLogger()
root_log.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # Command line arguments
    parser = argparse.ArgumentParser(description='Scrape')
    parser.add_argument('url', type=str, help='URL')
    parser.add_argument('--debug', action='store_true', help='include debug output')
    args = parser.parse_args()

    # Setup logging
    sh = logging.StreamHandler(sys.stdout)
    if args.debug:
        sh.setLevel(logging.DEBUG)
    else:
        sh.setLevel(logging.INFO)
    sh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    root_log.addHandler(sh)

    # Init scraper
    scrape = Scrape(ZivityScraper(root_log), root_log)

    # Download page
    if os.path.exists(args.url):
        scrape.scrape_file(args.url)
    else:
        scrape.scrape_url(args.url)

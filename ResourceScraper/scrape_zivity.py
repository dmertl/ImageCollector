import logging
import argparse
import os
import sys

from scrape import Scrape
from zivity import ZivityScraper

root_log = logging.getLogger()
root_log.setLevel(logging.DEBUG)


# def scrape_url(url):
#     root_log.info('Scraping URL {0}'.format(url))
#     html = urllib2.urlopen(url).read()
#     if html:
#         # Assumes URL of https://www.zivity.com/models/wolfsoul/photosets/1
#         model = url.split('/')[-3]
#         photoset = url.split('/')[-1]
#         scrape_html(html, model, photoset)
#     else:
#         raise IOError('Unable to download html from url {0}'.format(url))
#
#
# def scrape_html(html, model, photoset):
#     soup = BeautifulSoup(html)
#     resources = gather_resources(soup)
#     for resource in resources:
#         massaged = massage_resource(resource)
#         res_data = download_resource(massaged)
#         store_resource(res_data, resource_filename(massaged), model, photoset)
#     pass
#
#
# def gather_resources(soup):
#     # Retrieve all resource URLs from page
#
#     # Function for matching class name in BS4
#     def match_class(target):
#         def do_match(tag):
#             classes = tag.get('class', [])
#             return all(c in classes for c in target)
#
#         return do_match
#
#     resources = []
#     # Find image thumbnail container
#     imgs = soup.find(match_class(["thumbnail-image-container"])).find_all("img")
#     root_log.info('Found {0} images'.format(len(imgs)))
#     for img in imgs:
#         src = img['src']
#         # Check img is actual photo from photoset
#         if src[0:len('/content/photosets/')] == '/content/photosets/':
#             resources.append(src)
#         else:
#             root_log.debug('Skipping non photoset img {0}'.format(src))
#     return resources
#
#
# def massage_resource(url):
#     # Do any necessary massaging to resource URL
#     # TODO: May need to pass more than URL?
#
#     return 'https://www.zivity.com' + url.replace('tn_', '')
#
#
# def download_resource(url):
#     # Download resource
#
#     root_log.info('Downloading resource at {0}'.format(url))
#     return urllib2.urlopen(url).read()
#
#
# def resource_filename(url):
#     # Generate resource filename from URL
#
#     # Grab filename from URL filename last / to ?
#     return url[url.rfind('/') + 1:url.rfind('?')]
#
#
# def store_resource(res_data, filename, model, photoset):
#     # Save resource in appropriate folder path
#     # TODO: May want some metadata too
#
#     # Organize dir by model/photoset_num
#     dir = os.path.join('scrape', model, photoset)
#     if not os.path.exists(dir):
#         os.makedirs(dir)
#     file_path = os.path.join(dir, filename)
#     with open(file_path, 'w') as fh:
#         fh.write(res_data)
#     root_log.debug('Saved resource to {0}'.format(file_path))
#     pass


if __name__ == '__main__':
    # Setup logging
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    sh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    root_log.addHandler(sh)

    # Command line arguments
    parser = argparse.ArgumentParser(description='Scrape')
    parser.add_argument('url', type=str, help='URL')
    # parser.add_argument('--pretty', action='store_true', help='pretty print JSON output')
    args = parser.parse_args()

    # Init scraper
    scrape = Scrape(ZivityScraper())

    # Download page
    if os.path.exists(args.url):
        scrape.scrape_file(args.url)
        # html = urllib2.urlopen('file:{0}'.format(urllib2.quote(os.path.abspath(args.url)))).read()
        # if html:
        #     scrape_html(html, 'Unknown', 1)
        # else:
        #     root_log.error('Unable to load {0}'.format(args.url))
    else:
        scrape.scrape_url(args.url)

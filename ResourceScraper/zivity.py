import os
from bs4 import BeautifulSoup

from scrape import HtmlImageScraper, Resource


class ZivityScraper(HtmlImageScraper):
    def __init__(self):
        # TODO: DI
        self.storage = ZivityStorage()

    def grab_url(self, url):
        contents, meta = super(ZivityScraper, self).grab_url(url)
        # Assumes URL of https://www.zivity.com/models/<model_name>/photosets/<photoset_num>
        meta['model_name'] = url.split('/')[-3]
        meta['photoset_num'] = url.split('/')[-1]
        return contents, meta

    def grab_file(self, file_path):
        contents, meta = super(ZivityScraper, self).grab_file(file_path)
        # TODO: may be able to gather from contents, but shouldn't matter
        meta['model_name'] = 'Unknown'
        meta['photoset_num'] = 'Unknown'
        return contents, meta

    def create_content_parser(self, contents):
        return BeautifulSoup(contents)

    def find_resource_links(self, parser, page_meta):
        # Function for matching class name in BS4
        def match_class(target):
            def do_match(tag):
                classes = tag.get('class', [])
                return all(c in classes for c in target)

            return do_match

        resources = []
        # Find image thumbnail container
        imgs = parser.find(match_class(["thumbnail-image-container"])).find_all("img")
        # root_log.info('Found {0} images'.format(len(imgs)))
        for img in imgs:
            src = img['src']
            # Check img is actual photo from photoset
            if src[0:len('/content/photosets/')] == '/content/photosets/':
                resources.append(src)
                # else:
                # root_log.debug('Skipping non photoset img {0}'.format(src))
        return resources

    def link_to_resource(self, resource_link, page_meta):
        """

        :param resource_link: Resource link.
        :type resource_link: str
        :param page_meta: Page metadata.
        :type page_meta: dict
        :return: Resource.
        :rtype: Resource
        """
        # Add domain and replace thumbnail prefix in link
        url = 'https://www.zivity.com{0}'.format(resource_link.replace('tn_', ''))
        return Resource(url, page_meta)

    def resource_needed(self, resource):
        # Resource is needed if not in storage
        return not self.storage.resource_exists(resource)

    def store_resource(self, resource, data):
        self.storage.store(resource, data)


# TODO: Create some parent classes for file/folder based storage
class ZivityStorage(object):
    def __init__(self):
        pass

    def resource_exists(self, resource):
        file_path, dir, filename = self.get_storage_info(resource)
        return os.path.exists(file_path)

    def store(self, resource, data):
        file_path, dir, filename = self.get_storage_info(resource)
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(file_path, 'w') as fh:
            fh.write(data)

    def get_storage_info(self, resource):
        url = resource.url
        filename = url[url.rfind('/') + 1:url.rfind('?')]
        model = resource.meta['model_name']
        photoset = resource.meta['photoset_num']
        dir = os.path.join('scrape', model, photoset)
        file_path = os.path.join(dir, filename)
        return file_path, dir, filename

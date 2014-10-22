import os
import urllib2
import abc
import logging


class Scrape(object):
    """
    Runs the standard scraping process. Uses provided Scraper to perform actual content parsing.
    """

    def __init__(self, scraper, logger):
        """

        :param scraper: Scraper used to perform scraping.
        :type scraper: Scraper
        :param logger: Logger.
        :type logger: logging.RootLogger
        :return:
        :rtype:
        """
        self.scraper = scraper
        self.logger = logger

    def scrape_url(self, url):
        """
        Scrape a page from a URL via HTTP.

        :param url: URL to page.
        :type url: str
        :return: Additional URLs to scrape
        :rtype: string[]
        """
        contents, meta = self.scraper.grab_url(url)
        return self.scrape_page(contents, meta)

    def scrape_file(self, path):
        """
        Scrape a page from a file on the local filesystem.

        :param path: Path to file.
        :type path: str
        :return: Additional URLs to scrape
        :rtype: string[]
        """
        contents, meta = self.scraper.grab_file(path)
        return self.scrape_page(contents, meta)

    def scrape_page(self, contents, content_meta):
        """
        Scrape a page.

        :param contents: Page content.
        :type contents: str
        :param content_meta: Metadata from content retrieval.
        :type content_meta: dict
        :return:
        :rtype:
        """
        parser = self.scraper.create_content_parser(contents)
        page_meta = self.scraper.get_page_metadata(parser, content_meta)

        resource_links = self.scraper.find_resource_links(parser, page_meta)
        self.logger.debug('Found {0} resource links'.format(len(resource_links)))
        for resource_link in resource_links:
            resource = self.scraper.link_to_resource(resource_link, page_meta)
            if self.scraper.resource_needed(resource):
                data = self.scraper.download_resource(resource)
                self.scraper.store_resource(resource, data)
                self.logger.info('Downloaded resource {0}'.format(resource))
            else:
                self.logger.debug('Skipping unneeded resource {0}'.format(resource))

        page_links = self.scraper.find_page_links(parser, page_meta)
        self.logger.debug('Found {0} page links'.format(len(page_links)))
        additional_urls = []
        for page_link in page_links:
            page = self.scraper.link_to_page(page_link, page_meta)
            if self.scraper.page_needed(page):
                additional_urls.append(page.url)
            else:
                self.logger.debug('Skipping unneeded page {0}'.format(page))
        return additional_urls


class Resource(object):
    """
    A resource found while scraping.
    """

    def __init__(self, url, meta):
        """

        :param url: Resource URL
        :type url: str
        :param meta: Resource metadata
        :type meta: dict
        :return:
        :rtype:
        """
        self.url = url
        self.meta = meta

    def __str__(self):
        return str(self.url)


class Page(object):
    """
    A page found while scraping.
    """

    def __init__(self, url, meta):
        """

        :param url: Page URL
        :type url: str
        :param meta: Page metadata
        :type meta: dict
        :return:
        :rtype:
        """
        self.url = url
        self.meta = meta

    def __str__(self):
        return str(self.url)


class Scraper(object):
    def __init__(self, logger):
        """

        :param logger: Logger.
        :type logger: logging.RootLogger
        :return:
        :rtype:
        """
        self.logger = logger

    def grab_url(self, url):
        """
        Retrieve page contents and metadata from a URL.

        :param url: Page URL
        :type url: str
        :return: contents, metadata
        :rtype: tuple
        """
        self.logger.info('Retrieving URL {0}'.format(url))
        contents = urllib2.urlopen(url).read()
        meta = {'url': url}
        return contents, meta

    def grab_file(self, file_path):
        """
        Retrieve page contents and metadata from a file on the local filesystem.

        :param file_path: Path to file.
        :type file_path: str
        :return: contents, metadata
        :rtype: tuple
        """
        self.logger.info('Retrieving file {0}'.format(file_path))
        contents = urllib2.urlopen('file:{0}'.format(urllib2.quote(os.path.abspath(file_path)))).read()
        meta = {'file_path': file_path}
        return contents, meta

    @abc.abstractmethod
    def create_content_parser(self, contents):
        """
        Create object that assists with content parsing.

        :param contents: Page contents.
        :type contents: str
        :return:
        :rtype:
        """
        pass

    def get_page_metadata(self, parser, content_meta):
        """
        Get metadata for a page.

        :param parser: Page content parser.
        :type parser:
        :param content_meta: Metadata from content retrieval.
        :type content_meta: dict
        :return: Page metadata.
        :rtype: dict
        """
        return content_meta

    @abc.abstractmethod
    def find_resource_links(self, parser, page_meta):
        """
        Find resources links in page. Definition of a resource link is left to Scraper implementation. Resource links
        can be snippets of HTML, URLs, decoded JSON data, etc.

        :param parser: Page content parser.
        :type parser:
        :param page_meta: Page metadata.
        :type page_meta: dict
        :return: Resource links
        :rtype: list
        """
        pass

    def link_to_resource(self, resource_link, page_meta):
        """
        Convert resource link to a Resource. Perform any necessary massaging of resource_link to usable URL. Parse
        useful info from resource_link into metadata.

        :param resource_link: Resource link.
        :type resource_link:
        :param page_meta: Page metadata.
        :type page_meta: dict
        :return: Resource.
        :rtype: Resource
        """
        return Resource(resource_link, page_meta)

    def resource_needed(self, resource):
        """
        Check if a resource needs to be downloaded.

        :param resource: Resource.
        :type resource: Resource
        :return: True if the resource needs to be downloaded.
        :rtype: bool
        """
        return True

    def download_resource(self, resource):
        """
        Download resource data.

        :param resource: Resource.
        :type resource: Resource
        :return: Resource data.
        :rtype: str
        """
        return urllib2.urlopen(resource.url).read()

    @abc.abstractmethod
    def store_resource(self, resource, data):
        """
        Store a resource.

        :param resource: Resource.
        :type resource: Resource
        :param data: Resource data.
        :type data: str
        :return:
        :rtype:
        """
        pass

    @abc.abstractmethod
    def find_page_links(self, parser, page_meta):
        """
        Find additional page links in page.

        :param parser: Page content parser.
        :type parser:
        :param page_meta: Page metadata.
        :type page_meta: dict
        :return: Page links.
        :rtype: list
        """
        pass

    def link_to_page(self, page_link, page_meta):
        """
        Convert resource link to a Page. Perform any necessary massaging of page_link to usable URL. Parse
        useful info from page_link into metadata.

        :param page_link: Page link.
        :type page_link:
        :param page_meta: Page metadata.
        :type page_meta: dict
        :return: Page.
        :rtype: Page
        """
        return Page(page_link, page_meta)

    @abc.abstractmethod
    def page_needed(self, page):
        """
        Check if a page needs to be scraped.

        :param page: Page.
        :type page: Page
        :return: True if page should be scraped.
        :rtype: bool
        """
        return True


class HtmlImageScraper(Scraper):
    pass


import urllib2
from BeautifulSoup import BeautifulSoup


class DeviantImageCollector:
    """
    Collects an image from a deviantart.com deviation page
    """

    def __init__(self):
        self.sources = [
            DeviantDownloadAnchorImageSource(),
            DeviantContentImgImageSource()
        ]

    def collect(self, url):
        soup = BeautifulSoup(urllib2.urlopen(url).read())
        # TODO: collect highest resolution image, not just first image
        for source in self.sources:
            image_url = source.find(soup)
            if image_url:
                return image_url
        raise Exception('No images found')


class SoupSource(object):
    """
    Retrieve data from a BeautifulSoup source
    """

    def __init__(self):
        self.find_attrs = {}

    def find(self, soup):
        if self.find_attrs:
            sources = soup.findAll(attrs=self.find_attrs)
            if sources:
                return sources[0]
            else:
                raise Exception('No sources found')
        else:
            raise NotImplementedError('Must specify self.find_attrs for SoupSource')


class SoupUrlSource(SoupSource):
    """
    Retrieve a URL from a BeautifulSoup source
    """

    def __init__(self):
        super(SoupUrlSource, self).__init__()
        self.url_attribute = None

    def find(self, soup):
        if self.url_attribute:
            source = super(SoupUrlSource, self).find(soup)
            url = source.get(self.url_attribute)
            if url:
                return url
            else:
                raise Exception('Unable to get "{}" attribute from source'.format(self.url_attribute))
        else:
            raise NotImplementedError('Must set self.url_attribute for SoupUrlSource')


class DeviantDownloadAnchorImageSource(SoupUrlSource):

    def __init__(self):
        super(DeviantDownloadAnchorImageSource, self).__init__()
        self.find_attrs = {
            'class': 'dev-page-button dev-page-button-with-text dev-page-download'
        }
        self.url_attribute = 'href'


class DeviantContentImgImageSource(SoupUrlSource):

    def __init__(self):
        super(DeviantContentImgImageSource, self).__init__()
        self.find_attrs = {
            'class': 'dev-content-full'
        }
        self.url_attribute = 'src'

if __name__ == '__main__':
    collector = DeviantImageCollector()

    image_url = collector.collect('http://davidrapozaart.deviantart.com/art/Dross-Ripper-202469640')

    print image_url

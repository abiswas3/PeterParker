import sys
sys.path.append('../')

from . import utils

from urllib.parse import urlparse
import validators
import numpy as np
from collections import Counter, defaultdict

from .document_extractor import DocumentExtractor

class LinkExtractor(DocumentExtractor):

    def __init__(self, **kwargs):

        super(LinkExtractor, self).__init__(**kwargs)
        # The blacklist is very much a link extractor problem
        self.blacklist = []
        self.crawl_ready = []
        self.links = set()
        
    def process_page(self,
                     url,
                     page,
                     schema_org_check=True,
                     **kwargs):

        super().process_page(url,
                             page,
                             schema_org_check=schema_org_check,
                             **kwargs)

        if self.bad_page:
            return
        
        self.get_links(**kwargs)


    def init_blacklist(self, blacklist):
        # FIXME: This changes based on the architecture of the system
        self.blacklist = blacklist


    def _is_relative(self, url):

        o = urlparse(url)

        if not o.scheme and url[0] == '/':
            return "{}://{}{}".format(urlparse(self.curr_url).scheme,
                                      urlparse(self.curr_url).netloc,
                                      url)

        return url

    def _in_domain(self, url):

        o = urlparse(url)
        if o.netloc == self.domain:
            return True

        return False


    def get_links(self, **kwargs):

        urls_crawled = set()
        if 'urls_crawled' in kwargs:
            if not isinstance(kwargs['urls_crawled'], set):
                urls_crawled = set(kwargs['urls_crawled'])
            else:
                urls_crawled = kwargs['urls_crawled']

        base = urlparse(self.curr_url)
        self.domain = base.netloc

        # getting all links
        links = [x.attrib['href'] if 'href' in x.attrib else "" for x in self.tree.xpath('//a')]


        def bad_links(x):
            if x =='#' or x == '/' or not len(x):
                return False

            if '.jpg' in x or '.png' in x or '.svg' in x:
                return False

            return True

        # Deleting the null links
        self.links = [link for link in filter(bad_links, links)]

        self.links = set([self._is_relative(url) for url in self.links])
        self.crawl_ready = [url for url in self.links if validators.url(url) and url not in urls_crawled]

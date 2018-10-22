# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from delib_link_spiders.items import BulkLink
from scrapy.http import Request
import os

class BulkLinkSpider(CrawlSpider):
    name = 'bulk_link_spider'
    allowed_domains = ['bechy.fr', 'metz.fr']
    start_urls = ['http://www.bechy.fr/cr_conseil_municipal', 'https://metz.fr/projets/conseil_municipal/seances.php']

    rules = (Rule(LinkExtractor(), callback='parse_response', follow=False),)

    def parse_response(self, response):
        for link in LinkExtractor().extract_links(response):
            bulkLink = BulkLink()
            bulkLink['target_url'] = link.url
            bulkLink['text'] = link.text
            bulkLink['url'] = response.url
            yield(bulkLink)


class PdfSpider(CrawlSpider):
    name = 'pdf_spider'
    __allowed_domain = ''

    def __init__(self, *args, **kwargs):
        super(PdfSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]
        self.__allowed_domain = kwargs.get('allowed_domain')
        self.allowed_domains = [self.__allowed_domain]
        self.__create_directory()

    def __create_directory(self):
        if not os.path.exists('../data/pdf/' + self.__allowed_domain):
            os.makedirs('../data/pdf/' + self.__allowed_domain)

    rules = (Rule(LinkExtractor(), callback='parse_response', follow=False),)

    def parse_response(self, response):
        for href in response.css('a[href$=".pdf"]::attr(href)').extract():
            yield Request(
                url=response.urljoin(href),
                callback=self.save_pdf
            )

    def save_pdf(self, response):
        path = '../data/pdf/' + self.__allowed_domain + "/" + response.url.split('/')[-1]
        self.logger.info('Saving PDF %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)
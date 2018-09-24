# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from delib_link_spiders.items import BulkLink
import logging


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

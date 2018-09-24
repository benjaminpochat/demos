# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BulkLink(scrapy.Item):
    text = scrapy.Field()
    target_url = scrapy.Field()
    url = scrapy.Field()

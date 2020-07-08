# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AiiItem(scrapy.Item):
    # define the fields for your item here like:
    spider = scrapy.Field()
    
    title = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()

    file_urls = scrapy.Field()
    file = scrapy.Field()

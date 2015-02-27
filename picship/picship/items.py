# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PicshipItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	word = scrapy.Field()
	img_urls = scrapy.Field()

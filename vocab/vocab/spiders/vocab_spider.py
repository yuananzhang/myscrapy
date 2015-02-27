#! /usr/bin/python
# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from vocab.items import VocabItem 
from sets import Set
import re

class VocabSpider(CrawlSpider):
	name = "vocab"
	content_path = '//div[@id="post-entry"]//div[@class="post-content"]'
	photographic_site= 'http://vocabmadeeasy.com'
	download_delay = 1
	allowed_domains = ["vocabmadeeasy.com"]
	#start_urls = ['http://vocabmadeeasy.com/2009/02/a-list-121-130/']
	#start_urls = ['http://vocabmadeeasy.com/2010/12/w-list-1-5-2/']
	#start_urls = ['http://vocabmadeeasy.com/2010/01/b-list-1-10/']
	start_urls = ['http://vocabmadeeasy.com/']
	link_pattern = re.compile('^http://vocabmadeeasy.com/\d{4}/\d{2}/[a-z]-list[^/]*/$')
	parsed_urls = Set() 

	def __init__(self):
		super(VocabSpider, self).__init__()
	
	def parse(self, response):
		print "*****"+response.url
		sel = Selector(response)
		links = sel.xpath('//a/@href').extract()
		for link in links:
			if self.link_pattern.match(link) and link not in self.parsed_urls:
				print "***link is:"+link
				self.parsed_urls.add(link)
				yield Request(link, self.parse)
		contents = sel.xpath(self.content_path).extract()
		for content in contents:
			item = VocabItem()
			item['url'] = response.url
			item['content'] = content
			yield item

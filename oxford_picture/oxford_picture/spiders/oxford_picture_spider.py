#! /usr/bin/python
# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from oxford_picture.items import OxfordPictureItem 
from sets import Set
import re

class OxfordPictureSpider(CrawlSpider):
	name = "oxford_picture"
	content_path = '//div[@id="entryContent"]//div[@class="top-g"]'
	photographic_site= 'http://www.oxfordlearnersdictionaries.com/wordlist/english/pictures'
	download_delay = 1
	allowed_domains = ["oxfordlearnersdictionaries.com"]
	#start_urls = ['http://www.oxfordlearnersdictionaries.com/wordlist/english/pictures/pics_A-B/']
	start_urls = []
	request_word = {'A-B':2,'C-D':3,'E-G':2,'H-K':2,'L-N':2,'O-P':2,'Q-R':1,'S':2,'T':2,'U-Z':1}
	link_pattern = re.compile('^http://www\.oxfordlearnersdictionaries\.com/definition/english/\w+$')
	parsed_urls = Set()

	def __init__(self):
		super(OxfordPictureSpider, self).__init__()
		for k,v in self.request_word.iteritems():
			total_url = self.photographic_site+'/pics_'+k
			self.start_urls.append(total_url)
			for i in range(2,v+1):
				url = "/?page=%d" % i
				total_url += url
				self.start_urls.append(total_url)

	def parse(self, response):
		print "*****"+response.url
		sel = Selector(response)
		if response.url.split('/')[-2]=='english':
			contents = sel.xpath(self.content_path).extract()
			for content in contents:
				item = OxfordPictureItem()
				item['url'] = response.url
				item['content'] = content
				yield item
		else:
			links = sel.xpath('//a/@href').extract()
			for link in links:
				if self.link_pattern.match(link) and link not in self.parsed_urls:
					self.parsed_urls.add(link)
					print "***link is:"+link
					yield Request(link, self.parse)

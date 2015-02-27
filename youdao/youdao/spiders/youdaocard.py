# -*- coding: utf-8 -*-
import scrapy
from youdao.items import YoudaoItem
from selenium import webdriver
import time
import re

class YoudaocardSpider(scrapy.Spider):
	name = "youdaocard"
	youdao_url = "http://xue.youdao.com"
	allowed_domains = ["youdao.com"]
	youdao_url = 'http://xue.youdao.com/card.a?method=allCards&page='
	start_urls = []
	pattern = re.compile('^\./card\.a\?index=\d+$')

	def __init__(self):
		super(YoudaocardSpider,self).__init__()
		for i in range(1,86):
			total_url = self.youdao_url+str(i) 
			self.start_urls.append(total_url)
		self.driver = webdriver.Firefox()
	
	def __del__(self):
		self.driver.close()

	def parse(self, response):
		urls = response.xpath('//div[@id="card-list"]//tr/td/a/@href').extract()
		for url in urls: 
			if not self.pattern.match(url):
				continue
			total_url = 'http://xue.youdao.com'+url[1:]
			print total_url
			self.driver.get(total_url)
			time.sleep(3)
			element = self.driver.find_element_by_xpath('//div[@class="heightWrapper"]/div[@class="img"]/img')
			img_url = element.get_attribute('src')
			print img_url
			if len(img_url)==0:
				continue
			we = self.driver.find_element_by_xpath('//div[@class="heightWrapper"]/div[@class="word"]/span')
			word = we.text
			print word
			item = YoudaoItem()
			item['url'] = img_url
			item['word'] = word
			yield item




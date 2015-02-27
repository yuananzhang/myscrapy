# -*- coding: utf-8 -*-
import scrapy
import psycopg2
from picship.items import PicshipItem
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class PicshipSpider(scrapy.Spider):
	name = "picship_spider"
	allowed_domains = ["picship.com"]
	#request_words = ['text', 'spy']
	request_words = [] 
	start_urls = (
			'http://www.picship.com/',
			)

	def __init__(self):
		super(PicshipSpider,self).__init__()
		self._get_words_from_db()
		self.driver = webdriver.Firefox()

	def __del__(self):
		self.driver.close()

	def _get_words_from_db(self):
		try:
			conn=psycopg2.connect("dbname='acenglish' user='admin' password='314159'")
		except:
			print "I am unable to connect to the database."
			return
		cur = conn.cursor()
		try:
			query = """SELECT distinct word FROM word_main_dictionary where level=10 and word not in (select distinct word from pic_ship) """ 
			cur.execute(query)
			res = cur.fetchall()
			for item in res:
				word = item[0]
				print word 
				self.request_words.append(word)
		except Exception as error:
				print error
		cur.close()
		conn.close()

	def parse(self, response):
		self.driver.get(response.url)
		for word in self.request_words:
			print word
			elem = self.driver.find_element_by_xpath('//input[@type="text"]')
			elem.clear()
			elem.send_keys(word)
			elem.send_keys(Keys.RETURN)
			time.sleep(3)
			elements = self.driver.find_elements_by_xpath('//li/div[@class="pic"]/span/a/img')
			if len(elements)==0:
				continue
			img_urls = []
			for e in elements:
				img_url = e.get_attribute('src')
				print img_url
				img_urls.append(img_url)
			item = PicshipItem()
			item['word'] = word 
			item['img_urls'] = img_urls
			yield item

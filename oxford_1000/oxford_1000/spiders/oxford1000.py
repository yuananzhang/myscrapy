# -*- coding: utf-8 -*-
import scrapy
import psycopg2


class Oxford1000Spider(scrapy.Spider):
	name = "oxford1000"
	allowed_domains = ["oxforddictionaries.com"]
	start_urls = []

	def __init__(self):
		super(Oxford1000Spider, self).__init__(self)
		try:
			self.conn=psycopg2.connect("dbname='acenglish' user='admin' password='314159'")
		except:
			print "I am unable to connect to the database."
			return
		self.cur = self.conn.cursor()
		for i in range(1,21):
			url = 'http://www.oxforddictionaries.com/top1000/english?page='+str(i)
			print url
			self.start_urls.append(url)

	def parse(self, response):
		words = response.xpath('//div[@class="contentItem"]//span[@class="arl_hw"]/text()').extract()
		for word in words:
			print word
			if len(word)==0:
				continue
			word = word.replace('\'', '\'\'')
			sql = """insert into oxford_1000_uk (word) values ('%s') """ % (word)
			self.cur.execute(sql)
			self.conn.commit()

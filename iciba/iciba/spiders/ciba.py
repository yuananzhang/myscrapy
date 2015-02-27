# -*- coding: utf-8 -*-
import scrapy
import psycopg2
import sys
from scrapy.selector import Selector


class CibaSpider(scrapy.Spider):
	name = "ciba"
	allowed_domains = ["iciba.com"]
	CIBA_URL = 'http://www.iciba.com/'
	start_urls = [
			]

	def __init__(self):
		try:
			self.conn=psycopg2.connect("dbname='acenglish' user='admin' password='314159'")
		except:
			print "I am unable to connect to the database."
			return
		self.cur = self.conn.cursor()
		self._get_words_from_db(self.cur)

	def __del__(self):
		self.cur.close()
		self.conn.close()

	def _get_words_from_db(self, cur):
		query = """select word from ciba_words where expression='' """
		cur.execute(query)
		res = cur.fetchall()
		for item in res:
			word = item[0]
			word = word.replace(' ', '_')
			total_url = self.CIBA_URL+word
			self.start_urls.append(total_url)

	def _write_ciba_word(self, cur, conn, word, expression):
		word = word.replace('\'', '\'\'')
		expression = expression.replace('\'', '\'\'')
		try:
			sql = """update ciba_words set expression='%s' where word='%s' """ % (expression, word)
			cur.execute(sql)
			conn.commit()
		except Exception as error:
			print error
			sys.exit()

	def _parse_sentence(self, sentence):
		sel = Selector(text=sentence)
		return ''.join([text.strip() for text in sel.xpath('//text()').extract()])

	def parse(self, response):
		print response.url
		word = response.url.split('/')[-1].replace('_', ' ')
		print word
		sentences = response.xpath('//div[@class="group_prons"]/div[@class="group_pos"]/p').extract()
		expression = ''
		for sentence in sentences:
			expression += self._parse_sentence(sentence)
			expression += '\n'
		expression = expression.strip()
		print expression
		self._write_ciba_word(self.cur, self.conn, word, expression)


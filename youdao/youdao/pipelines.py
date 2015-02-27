# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from models import YoudaoCard, db_connect, create_youdao_table
from scrapy.selector import Selector
import urllib2

class YoudaoPipeline(object):
	def _get_picture(self, card, url):
		try:
			hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
					'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
					'Accept-Encoding': 'none',
					'Accept-Language': 'en-US,en;q=0.8',
					'Connection': 'keep-alive'}
			req = urllib2.Request(url, headers=hdr)
			resp = urllib2.urlopen(req, timeout=15)
			card.picture = resp.read()
		except Exception as error:
			print error

	def process_item(self, item, spider):
		img_url = item['url']
		imgref_url = img_url
		word = item['word']
		writer = YoudaoWriter();
		card = YoudaoCard()
		card.word = word
		card.img_url = img_url
		card.imgref_url = imgref_url
		self._get_picture(card, img_url)
		writer.write(card)
		return item

class YoudaoWriter(object):
	def __init__(self):
		engine = db_connect()
		create_youdao_table(engine)
		self.Session = sessionmaker(bind=engine)

	def write(self, card):
		session = self.Session()

		try:
			session.add(card)
			session.commit()
		except:
			session.rollback()
			raise
		finally:
			session.close()

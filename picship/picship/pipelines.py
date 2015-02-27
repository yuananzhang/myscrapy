# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
#from models import PicshipTable, db_connect, create_picship_table
#from scrapy.selector import Selector
import urllib2
import psycopg2

class PicshipPipeline(object):
	def __init__(self):
		print '***init'
		super(PicshipPipeline, self).__init__()
		try:
			self.conn=psycopg2.connect("dbname='acenglish' user='admin' password='314159'")
		except:
			print "I am unable to connect to the database."
			return
		self.cursor = self.conn.cursor()
	
	def __del__(self):
		print '***del'
		if self.cursor:
			self.conn.commit()
			self.cursor.close()
			self.conn.close()

	def _get_picture(self, url):
		try:
			hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
					'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
					'Accept-Encoding': 'none',
					'Accept-Language': 'en-US,en;q=0.8',
					'Connection': 'keep-alive'}
			req = urllib2.Request(url, headers=hdr)
			resp = urllib2.urlopen(req, timeout=15)
			picture = resp.read()
		except Exception as error:
			print error
		return picture

	def process_item(self, item, spider):
		print '***process item'
		if not self.cursor:
			return item

		word = item['word']
		print word
		urls = item['img_urls']
		for url in urls:
			print url
			try:
				sql = """insert into pic_ship(word,img_url) values('%s','%s')""" % (word,url)
				self.cursor.execute(sql)
			except Exception as error:
				print error
		self.conn.commit()
		return item
"""
class PicshipWriter(object):
	def __init__(self):
		engine = db_connect()
		create_picship_table(engine)
		self.Session = sessionmaker(bind=engine)

	def write(self, picship):
		session = self.Session()

		try:
			session.add(picship)
			session.commit()
		except Exception as error:
			print error
			session.rollback()
			raise
		finally:
			session.close()
"""

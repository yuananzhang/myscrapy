# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from models import OxfordPicture, db_connect, create_oxford_picture_table
from scrapy.selector import Selector
import urllib2

class ExpressionFilterPipeline(object):
	def _get_picture(self, oxford_picture, url):
		try:
			hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
					'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
					'Accept-Encoding': 'none',
					'Accept-Language': 'en-US,en;q=0.8',
					'Connection': 'keep-alive'}
			req = urllib2.Request(url, headers=hdr)
			resp = urllib2.urlopen(req, timeout=15)
			oxford_picture.picture = resp.read()
		except Exception as error:
			print error

	def process_item(self, item, spider):
		content = item['content']
		writer = OxfordPictureWriter()
		oxford_picture = OxfordPicture()
		sel = Selector(text=content)
		word = ''.join(sel.xpath('//div[@class="webtop-g"]/h2//text()').extract()).strip()
		print word
		oxford_picture.word = word
		picture_url = sel.xpath('//div[@id="ox-enlarge"]/a/img/@src').extract()[0]
		print picture_url
		oxford_picture.img_url = picture_url 
		self._get_picture(oxford_picture, oxford_picture.img_url)
		oxford_picture.imgref_url = item['url']
		writer.write(oxford_picture)
		return item

class OxfordPictureWriter(object):
	def __init__(self):
		engine = db_connect()
		create_oxford_picture_table(engine)
		self.Session = sessionmaker(bind=engine)

	def write(self, photographic):
		session = self.Session()

		try:
			session.add(photographic)
			session.commit()
		except:
			session.rollback()
			raise
		finally:
			session.close()

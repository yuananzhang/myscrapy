# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from models import Vocab, db_connect, create_vocab_table
from scrapy.selector import Selector
import urllib2

class ExpressionFilterPipeline(object):
	def _get_picture(self, vocab, url):
		try:
			hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
					'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
					'Accept-Encoding': 'none',
					'Accept-Language': 'en-US,en;q=0.8',
					'Connection': 'keep-alive'}
			req = urllib2.Request(url, headers=hdr)
			resp = urllib2.urlopen(req, timeout=15)
			vocab.picture = resp.read()
		except Exception as error:
			print error

	def _judge_picture(self, html, vocab):
		sel = Selector(text=html)
		pictures = sel.xpath('.//p//img/@src').extract()
		widths = sel.xpath('.//p//img/@width').extract()
		for i in range(len(pictures)):
			if int(widths[i])>=50:
				vocab.img_url = pictures[i]
				print vocab.img_url
				self._get_picture(vocab, vocab.img_url)
				return	
		other_pictures = sel.xpath('.//div/img/@src').extract()
		other_widths = sel.xpath('.//div/img/@width').extract()
		if len(other_pictures)!=len(other_widths):
			return
		for i in range(len(other_pictures)):
			if int(other_widths[i])>=50:
				vocab.img_url = other_pictures[i]
				print vocab.img_url
				self._get_picture(vocab, vocab.img_url)
				break
	
	def _process_picture(self, sel, vocab, start_index, end_index):
		for i in range(start_index, end_index+1):
			path_str = './/div[@class="post-content"]/*[%d]' % i
			html = sel.xpath(path_str).extract()[0]
			self._judge_picture(html, vocab)

	def _get_all_h1_index(self, sel, total):
		self.h1_indexs = []
		for i in range(total):
			path_str = './/div[@class="post-content"]/*[%d]' % (i+1)	
			html = sel.xpath(path_str).extract()[0]
			sel2 = Selector(text=html)
			if len(sel2.xpath('.//h1').extract())>0:
				self.h1_indexs.append(i+1)
		print self.h1_indexs
	
	def _get_h1_word(self, sel, index, vocab):
		path_str = './/div[@class="post-content"]/*[%d]' % index
		html = sel.xpath(path_str).extract()[0]
		sel2 = Selector(text=html)
		word = ''.join(sel2.xpath('.//h1//text()').extract()).strip().split(' ')[-1].lower()
		print word
		vocab.word = word

	def process_item(self, item, spider):
		content = item['content']
		sel = Selector(text=content)
		childs = sel.xpath('count(.//div[@class="post-content"]/*)').extract()[0]
		total = int(float(childs))
		print total 
		self._get_all_h1_index(sel, total)
		writer = VocabWriter()
		for i in range(len(self.h1_indexs)):
			vocab = Vocab()
			vocab.imgref_url = item['url']
			self._get_h1_word(sel, self.h1_indexs[i], vocab)
			start_index = self.h1_indexs[i]+1
			if i==(len(self.h1_indexs)-1):
				end_index = total
			else:
				end_index = self.h1_indexs[i+1]-1
			self._process_picture(sel, vocab, start_index, end_index)
			writer.write(vocab)
		return item

class VocabWriter(object):
	def __init__(self):
		engine = db_connect()
		create_vocab_table(engine)
		self.Session = sessionmaker(bind=engine)

	def write(self, vocab):
		session = self.Session()

		try:
			session.add(vocab)
			session.commit()
		except:
			session.rollback()
			raise
		finally:
			session.close()

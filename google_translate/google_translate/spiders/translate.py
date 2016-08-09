# -*- coding: utf-8 -*-

import scrapy
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from google_translate.models import RemoteTranslate, RemoteDb
from scrapy.utils.ossignal import install_shutdown_handlers

from scrapy import optional_features
# uncommented fixes my issue
optional_features.remove('boto')

import logging
selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
selenium_logger.setLevel(logging.WARNING)

class TranslateSpider(scrapy.Spider):
    name = "translate"
    allowed_domains = ["google.com.hk"]
    start_urls = (
        'https://translate.google.com.hk/',
    )

    def __init__(self):
        super(TranslateSpider, self).__init__()
        #profile = webdriver.FirefoxProfile('/Users/zhangyuanan/Library/Application Support/Firefox/Profiles/npdra49b.new')
        #self.driver = webdriver.Firefox(profile)
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)
        self.driver.implicitly_wait(10) 
        self.db = RemoteDb()
        self.force_quit = False
        install_shutdown_handlers(self._quit_func)

    def _quit_func(self, signum, _):
        print '****************quit func********'
        self.force_quit = True

    def parse(self, response):
        print response.url
        self.driver.get(response.url+'#en/zh-CN/')
        #sentences = ['defer','how are you?', 'what time is it now?', 'see you later!']
        pre_chinese = ''
        #for sentence in sentences:
        query = self.db.query()
        for item in query:
            if self.force_quit:
                break
            if item.id%5!=0:
                continue
            print item.english, item.id
            try:
                source = self.driver.find_element_by_xpath('//textarea[@id="source"]')
                source.clear()
                source.send_keys(item.english)
                submit = self.driver.find_element_by_xpath('//input[@id="gt-submit"]')
                submit.send_keys(Keys.RETURN)
                time.sleep(2)
                results = self.driver.find_elements_by_xpath('//span[@id="result_box"]/span')
            except Exception as error:
                print '********error*****'
                print error
                continue
            chinese = ''
            for result in results:
                chinese += result.text
            if chinese==pre_chinese:
                print '******don\'t get translate words****'
            else:
                print chinese
                self.db.update(RemoteTranslate(hash=item.hash, english=item.english, chinese=chinese.encode('utf-8')))
                pre_chinese = chinese

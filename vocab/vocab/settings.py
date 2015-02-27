# -*- coding: utf-8 -*-

# Scrapy settings for vocab project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'vocab'

SPIDER_MODULES = ['vocab.spiders']
NEWSPIDER_MODULE = 'vocab.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'acenglish (+http://www.zimucheng.com)'

COOKIES_ENABLES = False
LOG_LEVEL = 'INFO'

ITEM_PIPELINES = {
		'vocab.pipelines.ExpressionFilterPipeline' : 300,
		}

DOWNLOADER_MIDDLEWARES = {
		'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 100,
		'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': 200,
		}

ROBOTSTXT_OBEY = True

DATABASE = {'drivername': 'postgres',
		'host': 'localhost',
		'port': '5432',
		'username': 'admin',
		'password': '314159',
		'database': 'acenglish'}

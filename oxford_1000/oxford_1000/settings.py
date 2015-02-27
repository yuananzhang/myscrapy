# -*- coding: utf-8 -*-

# Scrapy settings for oxford_1000 project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'oxford_1000'

SPIDER_MODULES = ['oxford_1000.spiders']
NEWSPIDER_MODULE = 'oxford_1000.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'oxford_1000 (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
		        'oxford_1000.pipelines.Oxford1000Pipeline' : 400,
				        }

DATABASE = {'drivername': 'postgres',
		'host': 'localhost',
		'port': '5432',
		'username': 'admin',
		'password': '314159',
		'database': 'acenglish'}

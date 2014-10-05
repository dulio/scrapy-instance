# -*- coding: utf-8 -*-

# Scrapy settings for douban_movie project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'douban_book'

SPIDER_MODULES = ['douban_book.spiders']
NEWSPIDER_MODULE = 'douban_book.spiders'
ITEM_PIPELINES={
  'douban_book.pipelines.DoubanBookPipeline':400,
}
LOG_LEVEL='WARNING'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'douban_movie (+http://www.yourdomain.com)'
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
COOKIES_ENABLED = True

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DoubanBookItem(scrapy.Item):
    name = scrapy.Field() 
    origin_name = scrapy.Field()
    score = scrapy.Field()
    author = scrapy.Field()
    info = scrapy.Field()
    description = scrapy.Field()  # 内容
    description_hidden = scrapy.Field()  #隐藏内容
    description2 = scrapy.Field()  # 内容
    description_hidden2 = scrapy.Field()  #隐藏内容

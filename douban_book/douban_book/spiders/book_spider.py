# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from douban_book.items import DoubanBookItem

class BookSpider(CrawlSpider):
  name="douban_book"
  allowed_domains=["book.douban.com"]
  url=r'http://book.douban.com/tag/'
  #url=r'http://book.douban.com/tag/%E5%B0%8F%E8%AF%B4'
  #url=r'http://book.douban.com/subject/10594787/'
  start_urls=[url]
  rules=[
    Rule(SgmlLinkExtractor(allow=(url+r'[\u4e00-\u9fa5]+',))),
    Rule(SgmlLinkExtractor(allow=(url+r'.+\?start=\d+.*',))),
    Rule(SgmlLinkExtractor(allow=(r'^http://book.douban.com/subject/\d+/$',)),callback="parse_item"),
  ]

  def parse_item(self,response):
    sel=Selector(response)
    item=DoubanBookItem()
    item['name']=sel.xpath('//*[@id="wrapper"]/h1/span/text()').extract()
    item['author']=sel.xpath('//*[@id="info"]/span[1]/a/text()').extract()
    item['info']=sel.xpath('//*[@id="info"]').re(r'<span class="pl">(.+):</span>(.+)<br>')
    item['score']=sel.xpath('//*[@id="interest_sectl"]/div/p[1]/strong/text()').extract()
    item['author_description']= sel.xpath('//*[@id="content"]/div/div[1]/div[3]/div[2]/div/div/p/text()').extract()
    item['author_description_hidden']= sel.xpath('//*[@id="content"]/div/div[1]/div[3]/div[2]/span[2]/div/p/text()').extract()
    item['description']= sel.xpath('//*[@id="link-report"]/div[1]/div/p/text()').extract()
    item['description_hidden']= sel.xpath('//*[@id="link-report"]/span[2]/div/div/p/text()').extract()
    return item

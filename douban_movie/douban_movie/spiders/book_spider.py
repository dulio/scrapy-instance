# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from douban_movie.items import DoubanMovieItem

class BookSpider(CrawlSpider):
  name="douban_book"
  allowed_domains=["book.douban.com"]
  url=r'http://book.douban.com/tag/'
  start_urls=[url]
  rules=[
    Rule(SgmlLinkExtractor(allow=(url+r'[\u4e00-\u9fa5]+',))),
    Rule(SgmlLinkExtractor(allow=(url+r'.+\?start=\d+.*',))),
    Rule(SgmlLinkExtractor(allow=(r'http://book.douban.com/subject/\d+',)),callback="parse_item"),
  ]

  def parse_item(self,response):
    sel=Selector(response)
    item=DoubanMovieItem()
    item['name']=sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
    item['year']=sel.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
    item['score']=sel.xpath('//*[@id="interest_sectl"]/div/p[1]/strong/text()').extract()
    item['director']=sel.xpath('//*[@id="info"]/span[1]/a/text()').extract()
    item['classification']= sel.xpath('//span[@property="v:genre"]/text()').extract()
    item['actor']= sel.xpath('//*[@id="info"]/span[3]/a[1]/text()').extract()
    item['description']= sel.xpath('//*[@id="link-report"]/span[1]/text()').extract()
    item['description_hidden']= sel.xpath('//*[@id="link-report"]/span[2]/text()').extract()
    return item

# -*- coding: utf-8 -*-
import time
from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request

import MySQLdb
import MySQLdb.cursors

class DoubanBookPipeline(object):
  def __init__(self):
    self.dbpool = adbapi.ConnectionPool('MySQLdb',
        host = '192.168.33.10',
        db = 'data',
        user = 'root',
        passwd = '12345',
        cursorclass = MySQLdb.cursors.DictCursor,
        charset = 'utf8',
        use_unicode = False
    )
  def process_item(self, item, spider):
    query = self.dbpool.runInteraction(self._conditional_insert, item)
    query.addErrback(self.handle_error)
    return item

  def _conditional_insert(self,tx,item):
    tx.execute("select * from douban_book where name= %s",(item['name'][0],))
    result=tx.fetchone()
    log.msg(result,level=log.DEBUG)
    #print item
    if result:
      log.msg("Item already stored in db:%s" % item,level=log.DEBUG)
      print '[FAIED] book [%s] existed.' % (item['name'][0])
    else:
      # if description is empty
      desc=author_desc=origin_name=date=isbn=author=''
      gmt=time.time()
      
      if item['description_hidden']:
        item['description']=item['description_hidden']
      if not item['description']:
        item['description']=item['description2']
      lenDesc=len(item['description'])
      for n in xrange(lenDesc):
        desc+=item['description'][n].strip()
        if n<lenDesc-1:
          desc+='\n'

      lenInfo=len(item['info'])
      for n in xrange(lenInfo):
        # 原作名
        if item['info'][n] == u'\u539f\u4f5c\u540d':
          origin_name = item['info'][n+1].strip()
        # 发行日期
        if item['info'][n] == u'\u51fa\u7248\u5e74':
          date = item['info'][n+1].strip()
        # isbn
        if item['info'][n] == u'ISBN':
          isbn = item['info'][n+1].strip()
      
      tx.execute(\
        "insert into douban_book (name,origin_name,score,`date`,isbn,author,description,gmt_create,gmt_modified) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",\
        (item['name'][0],origin_name,item['score'][0],date,isbn,item['author'][0],desc,gmt,gmt))
      print '[SUCCESS] movie [%s].' % (item['name'][0])
      log.msg("Item stored in db: %s" % item, level=log.DEBUG)

  def handle_error(self, e):
    log.err(e)

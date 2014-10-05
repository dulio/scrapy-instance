# -*- coding: utf-8 -*-
import time
from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request

import MySQLdb
import MySQLdb.cursors

class DoubanMoviePipeline(object):
  def __init__(self):
    self.dbpool = adbapi.ConnectionPool('MySQLdb',
        host = '192.168.2.50',
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
    tx.execute("select * from douban_movie where name= %s",(item['name'][0],))
    result=tx.fetchone()
    log.msg(result,level=log.DEBUG)
    #print result
    if result:
      log.msg("Item already stored in db:%s" % item,level=log.DEBUG)
      print '[FAIED] movie [%s] existed.' % (item['name'][0])
    else:
      classification=actor=desc=''
      gmt=time.time()
      lenClassification=len(item['classification'])
      lenActor=len(item['actor'])
      for n in xrange(lenClassification):
        classification+=item['classification'][n]
        if n<lenClassification-1:
          classification+='/'
      for n in xrange(lenActor):
        actor+=item['actor'][n]
        if n<lenActor-1:
          actor+='/'
      
      # if description is empty
      if item['description_hidden']:
        item['description']=item['description_hidden']
      
      lenDesc=len(item['description'])
      for n in xrange(lenDesc):
        desc+=item['description'][n].strip()
        if n<lenDesc-1:
          desc+='\n'

      tx.execute(\
        "insert into douban_movie (name,year,score,director,classification,actor,description,gmt_create,gmt_modified) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",\
        (item['name'][0],item['year'][0],item['score'][0],item['director'][0],classification,actor,desc,gmt,gmt))
      print '[SUCCESS] movie [%s].' % (item['name'][0])
      log.msg("Item stored in db: %s" % item, level=log.DEBUG)

  def handle_error(self, e):
    log.err(e)

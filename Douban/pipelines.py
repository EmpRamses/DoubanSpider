# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

def dbHandle( ):
    conn = pymysql.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'root',
        charset = 'utf8',
        use_unicode = False
    )
    return conn

class DoubanPipeline(object):
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        sql = 'INSERT INTO douban.movies(title, href) VALUE (%s,%s)'

        try:
            cursor.execute(sql, (item['title'],item['href']))
            dbObject.commit()
        except Exception as e:
            print(e)
            dbObject.rollback()
        return item

class CommentsPipeline(object):
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        sql = 'INSERT INTO douban.review(mid, title, pid, pname, rating) VALUE (%s, %s, %s, %s, %s)'

        try:
            cursor.execute(sql, (item['mid'],item['title'],item['pid'],item['pname'],item['rating']))
            dbObject.commit()
        except Exception as e:
            print(e)
            dbObject.rollback()
        return item

class ContactsPipeline(object):
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        sql = 'INSERT INTO douban.links(pid, pname, lid, link) VALUE (%s, %s, %s, %s)'

        try:
            cursor.execute(sql, (item['pid'],item['pname'],item['lik'],item['link']))
            dbObject.commit()
        except Exception as e:
            print(e)
            dbObject.rollback()
        return item
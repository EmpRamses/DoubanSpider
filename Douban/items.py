# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
    pass

class CommentsItem(scrapy.Item):
    mid = scrapy.Field()
    title = scrapy.Field()
    pid = scrapy.Field()
    pname = scrapy.Field()
    rating = scrapy.Field()
    pass

class ContactsItem(scrapy.Item):
    pid = scrapy.Field()
    pname = scrapy.Field()
    lid = scrapy.Field()
    link = scrapy.Field()
    pass

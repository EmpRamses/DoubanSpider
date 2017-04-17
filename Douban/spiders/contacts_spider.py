# encoding utf-8
import scrapy
import pymysql

from Douban.items import ContactsItem


def dbHandle ():
    conn = pymysql.connect (
        host='localhost' ,
        user='root' ,
        passwd='root' ,
        db='douban'
    )
    return conn


class ContactsSpider ( scrapy.Spider ):
    name = 'contacts'
    allowed_domain = ["movie.douban.com"]
    start_urls = []
    dbObject = dbHandle ( )
    cursor = dbObject.cursor ( )
    cursor.execute ( "SELECT pid FROM review" )
    pids = cursor.fetchall ( )
    for i in range ( 0 , len ( pids ) ):
        hrefstr = 'https://www.douban.com/people/' + str ( pids[i] ) + '/contacts'
        start_urls.append ( hrefstr )

    def make_requests_from_url ( self , url ):
        Cookie = {'bid': 'DLVe9Sev_8' ,
                  'll': "108288" ,
                  'gr_user_id': 'bf750e17-5b95-4378-870b-7cdcdcec5c6b' ,
                  'ct': 'y' ,
                  'ps': 'y' ,
                  '_vwo_uuid_v2': 'C487926DE75356DF983BB93FE49ACEC5|23f732a12cb45bd1ad9ca3487c5b5e43' ,
                  '__utmt': '1' ,
                  'ue': 'qqn4679322yo@163.com' ,
                  'dbcl2': '160044020:b/R2DzEtIbg' ,
                  'ck': 'fG4v' ,
                  'push_noty_num': '0' ,
                  'push_doumail_num': '0' ,
                  '_pk_id.100001.4cf6': '9611b550465e1d94.1488285998.37.1491785685.1491724796.' ,
                  '_pk_ses.100001.4cf6': '*' ,
                  '__utmv': '30149280.16004' ,
                  'ap': '1' , }
        return scrapy.Request ( url , cookies=Cookie )

    def parse ( self , response ):
        # print(response.body)
        selector = scrapy.Selector ( response )
        pid = selector.xpath('//div[@class="pic"]/a/@href').extract_first( )
        pid = pid[30:-1]
        pname = selector.xpath('//div[@class="pic"]/a/img/@alt').extract_first( )
        for contacts in selector.xpath ( '//dl[@class="obu"]' ):
            link = contacts.xpath ( './dd/a/text()' ).extract_first ( )
            if link != '[已注销]':
                lid = contacts.xpath ( './dd/a/@href' ).extract_first ( )
                lid = lid[30:-1]
                item = ContactsItem ( )
                item['pid'] = pid
                item['pname'] = pname
                item['lid'] = lid
                item['link'] = link
                yield item

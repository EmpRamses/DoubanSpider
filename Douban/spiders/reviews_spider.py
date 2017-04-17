# encoding utf-8
# CommentsPipline
import scrapy
import pymysql

from Douban.items import CommentsItem


def dbHandle ():
    conn = pymysql.connect (
        host='localhost' ,
        user='root' ,
        passwd='root' ,
        db='douban'
    )
    return conn


class ReviewsSpider ( scrapy.Spider ):
    name = 'reviews'
    allowed_domain = ["movie.douban.com"]
    start_urls = []
    dbObject = dbHandle ( )
    cursor = dbObject.cursor ( )
    cursor.execute ( "SELECT href FROM movies" )
    href = cursor.fetchall ( )
    for i in range ( 0 , len(href) ):
        hrefstr = str ( href[i] )[2:-3] + 'reviews'
        start_urls.append ( hrefstr )

    def parse ( self , response ):
        # print(response.body)
        selector = scrapy.Selector ( response )
        fold = selector.xpath('//div[@class="fold-hd"]')
        if fold.__len__() == 0 :
            info = selector.xpath ( '//div[@class="subject-img"]' )
            mid = info.xpath ( './a/@href' ).extract_first ( )
            mid = mid[-9:-1]
            title = info.xpath ( './a/img/@title' ).extract_first ( )
            for review in selector.xpath ( '//div[@class="header-more"]' ):
                item = CommentsItem ( )
                pid = review.xpath ( './a[2]/@href' ).extract_first ( )
                pid = pid[30:-1]
                pname = review.xpath ( './a[2]/span/text()' ).extract_first ( )
                rate = review.xpath ( './span[1]/@title' ).extract_first ( )
                if rate == '力荐':
                    rating = 5
                elif rate == '推荐':
                    rating = 4
                elif rate == '还行':
                    rating = 3
                elif rate == '较差':
                    rating = 2
                else:
                    rating = 1
                item['mid'] = mid
                item['title'] = title
                item['pid'] = pid
                item['pname'] = pname
                item['rating'] = rating
                yield item
            pre_url = 'https://movie.douban.com/subject/' + mid + '/reviews'
            next_page_url = pre_url + response.xpath ( '//span[@class="next"]/a/@href' ).extract_first ( )
            if next_page_url is not pre_url:
                yield scrapy.Request ( response.urljoin ( next_page_url ) )

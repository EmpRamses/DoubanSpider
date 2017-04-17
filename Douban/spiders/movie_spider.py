# encoding utf-8
import scrapy

from Douban.items import DoubanItem

class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/tag/2015?start=0&type=T"]

    def parse(self, response):
        #print(response.body)
        selector = scrapy.Selector ( response )
        for movie in selector.xpath('//tr[@class="item"]'):
            item = DoubanItem( )
            title = movie.xpath( './td[1]/a/@title' ).extract_first()
            href = movie.xpath('./td[1]/a/@href').extract_first()
            item['title'] = title
            item['href'] = href
            #print(title)
            #print(href)
            yield item
        #startnum = response.url
        #startnum = startnum[40:-7]
        #num = int(startnum) + 20
        #next_page_url = 'https://movie.douban.com/tag/2015?start=' + str(num) + '&type=O'
        next_page_url = response.xpath('//span[@class="next"]/a/@href').extract_first()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url))
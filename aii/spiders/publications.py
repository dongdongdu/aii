# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from aii.items import AiiItem
import hashlib


class PublicationsSpider(scrapy.Spider):
    name = 'publications'
    allowed_domains = ['aii-alliance.org']

    start_urls = ['http://www.aii-alliance.org/index.php?m=content&c=index&a=lists&catid=24&page=1']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        body = response.body

        list = Selector(text=body).css('ul.Meeting_box a').extract()

        for li in list:
            itm = AiiItem()
            link = Selector(text=li).css('a').xpath('@href').extract()
            date_list = Selector(text=li).xpath('//div/text()').extract()

            if (len(date_list) * len(link)) > 0:
                itm['link'] = link[0]
                itm['url_hash'] = hashlib.md5(link[0].encode('utf-8')).hexdigest()
                itm['date'] = date_list[-1][1:]
                yield scrapy.Request(url=itm['link'], meta={'itm': itm}, callback=self.parse)

        next_page_url = Selector(text=body).css('#pages a:last-child').xpath('@href').extract()
        if len(next_page_url) > 0:
            next_page_url = 'http://www.aii-alliance.org/' + next_page_url[0]
            if next_page_url != response.request.url:
                yield scrapy.Request(url=next_page_url, callback=self.parse_list)

    def parse(self, response):
        itm = response.meta['itm']
        body = response.body

        itm['title'] = Selector(text=body).css('div.news-content h2').xpath('text()').extract()[0]

        file_url = Selector(text=body).css('div.news-content > a').xpath('@href').extract()

        itm['content'] = Selector(text=body).css('div.news-content').extract()[0]
        
        if len(file_url) > 0:
            itm['file_urls'] = ['http://www.aii-alliance.org/' + file_url[0]]
        else:
            itm['file_urls'] = []

        yield itm

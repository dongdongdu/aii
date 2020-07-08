# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from aii.items import AiiItem


class FilesSpider(scrapy.Spider):
    name = 'files'
    allowed_domains = ['aii-alliance.org']

    # start_urls = ['http://aii-alliance.org/index.php?m=content&c=index&a=lists&catid=23&page=1']

    def start_requests(self):

        # white papers
        page = 2
        for i in range(1, page + 1):
            url = 'http://www.aii-alliance.org/index.php?m=content&c=index&a=lists&catid=23&page=' + str(i)
            yield scrapy.Request(url=url, callback=self.parse_list)

            # # Publications
            # page = 2
            # url = 'http://www.aii-alliance.org/index.php?m=content&c=index&a=lists&catid=23&page=' + str(i)
            # for i in range(1, page + 1):
            #     # url = 'http://www.aii-alliance.org/index.php?m=content&c=index&a=lists&catid=23&page=' + str(i)
            #     yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        body = response.body

        list = Selector(text=body).css('ul.Meeting_box a').extract()

        for li in list:
            itm = AiiItem()
            link = Selector(text=li).css('a').xpath('@href').extract()
            date_list = Selector(text=li).xpath('//div/text()').extract()

            if (len(date_list) * len(link)) > 0:
                itm['link'] = link[0]
                itm['date'] = date_list[-1][1:]
                yield scrapy.Request(url=itm['link'], meta={'itm': itm}, callback=self.parse)

    def parse(self, response):
        itm = response.meta['itm']

        body = response.body
        itm['title'] = Selector(text=body).css('div.news-content h2').xpath('text()').extract()[0]
        itm['file_urls'] = ['http://www.aii-alliance.org/' + \
                            Selector(text=body).css('div.news-content a').xpath('@href').extract()[0]]
        yield itm

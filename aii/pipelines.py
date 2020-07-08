# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.files import FilesPipeline
from os.path import join
import scrapy


class AiiAddSpiderNamePipeline(object):
    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        item['spider'] = spider.name
        return item


class AiiFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield scrapy.Request(file_url, meta={'itm': item}, callback=self.file_path)

    def file_path(self, request, response=None, info=None):
        itm = request.meta['itm']
        file_name = itm['title'] + '-' + itm['date'] + '.pdf'

        # remove special file name characters
        file_name.replace("/", "-")
        file_name.replace("'", "")
        file_name.replace('"', '')

        return file_name

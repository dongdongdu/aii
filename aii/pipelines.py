# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.files import FilesPipeline
from os.path import join
import scrapy
import sqlite3
import datetime
from aii import settings
from scrapy.exceptions import DropItem
import logging


class AiiAddSpiderNamePipeline(object):
    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        item['spider'] = spider.name
        return item


class AiiDuplicateItemPipeline(object):
    logger = logging.getLogger("AiiDuplicateItemPipeline")

    def open_spider(self, spider):
        self.conn = sqlite3.connect(settings.SQLITE_DB_FILE)
        self.cursor = self.conn.cursor()

        sql = 'CREATE TABLE IF NOT EXISTS aii_items (' \
              'url_hash varchar(40),' \
              'title text,' \
              'date date,' \
              'link text,' \
              'file_urls text,' \
              'spider varchar(20))'

        self.cursor.execute(sql)
        self.conn.commit()

        self.new_item_count = 0
        self.duplicated_item_count = 0

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

        self.logger.info("Spider " + spider.name + ' New added item count is {}'.format(self.new_item_count))
        self.logger.info("Spider " + spider.name + 'Duplicated item count is {}'.format(self.duplicated_item_count))
        self.logger.info(
            "Spider " + spider.name + 'Total item count is {}'.format(self.new_item_count + self.duplicated_item_count))

    def process_item(self, item, spider):
        url_hash = item['url_hash']

        sql = "select url_hash from aii_items where url_hash = '" + url_hash + "'"
        res = self.cursor.execute(sql).fetchall()
        if len(res) > 0:
            self.duplicated_item_count = self.duplicated_item_count + 1
            raise DropItem("Found duplicated item {}".format(item['title']))
        else:

            values = (item['url_hash'],
                      item['title'],
                      datetime.datetime.strptime(item['date'], "%Y.%m.%d"),
                      item['link'],
                      str(item['file_urls']),
                      item['spider'])

            sql = "INSERT INTO aii_items VALUES (?,?,?,?,?,?)"
            self.cursor.execute(sql, values)
            self.conn.commit()

            self.new_item_count = self.new_item_count + 1
            return item


class AiiFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if len(item['file_urls']) > 0:
            for file_url in item['file_urls']:
                yield scrapy.Request(file_url, meta={'itm': item}, callback=self.file_path)
        else:
            item['files'] = []

    def file_path(self, request, response=None, info=None):
        itm = request.meta['itm']
        file_name = itm['title'] + '-' + itm['date'] + '.pdf'

        # remove special file name characters

        file_name = file_name.replace(":", "")
        file_name = file_name.replace("/", "")
        file_name = file_name.replace("'", "")
        file_name = file_name.replace('"', '')
        file_name = file_name.replace('|', '-')

        file_name = itm['spider'] + '/' + file_name
        return file_name

# -*- coding: utf-8 -*-


import logging
from scrapy import logformatter


class PoliteLogFormatter(logformatter.LogFormatter):
    def dropped(self, item, exception, response, spider):
        return {
            'level': logging.INFO,  # lowering the level from logging.WARNING
            'msg': u"Dropped Item: {}".format(item['title']),
            'args': {
                'exception': exception,
                'item': item,
            }
        }

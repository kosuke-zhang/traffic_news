#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : 张旭
# @Email   : zhangxu3486432@gmail.com
# @Blog    : https://zhangxu3486432.github.io
# @FileName: dupefilters.py
# @Time    : 2020/2/3

from __future__ import print_function

import logging

import pymysql
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
from scrapy.utils.request import referer_str, request_fingerprint


class RFPDupeFilter(BaseDupeFilter):
    """Request Fingerprint duplicates filter"""

    def __init__(self, database_name=None, table_name=None, filter_name=None, debug=False):
        self.fingerprints = set()
        self.logdupes = True
        self.debug = debug
        self.logger = logging.getLogger(__name__)
        self.fingerprints.update()
        if database_name and table_name:
            host = settings.get('MYSQL_HOST', 'localhost')
            mysql_user = settings.get('MYSQL_USER', 'root')
            mysql_pwd = settings.get('MYSQL_PASSWORD', 'news_crawler')
            mysql_port = settings.get('MYSQL_PORT', 3306)
            self.db = pymysql.connect(host, mysql_user, mysql_pwd, database_name, mysql_port)
            self.cursor = self.db.cursor()
            sql = "SELECT {0} FROM {1} WHERE 1".format(filter_name, table_name)
            self.cursor.execute(sql)
            ids = self.cursor.fetchall()
            self.fingerprints.update(ids)

    @classmethod
    def from_crawler(cls, crawler):
        debug = settings.getbool('DUPEFILTER_DEBUG')
        return cls(crawler.spider.database_name, crawler.spider.table_name, crawler.spider.filter_name, debug)

    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)

    def request_fingerprint(self, request):
        return request_fingerprint(request)

    def close(self, reason):
        if self.db and self.cursor:
            self.db.close()
            self.cursor.close()

    def log(self, request, spider):
        if self.debug:
            msg = "Filtered duplicate request: %(request)s (referer: %(referer)s)"
            args = {'request': request, 'referer': referer_str(request)}
            self.logger.debug(msg, args, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request: %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False

        spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)

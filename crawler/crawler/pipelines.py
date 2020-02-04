# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class SavePipeline(object):

    def __init__(self):
        host = settings.get('MYSQL_HOST', 'localhost')
        mysql_user = settings.get('MYSQL_USER', 'root')
        mysql_pwd = settings.get('MYSQL_PASSWORD', 'news_crawler')
        mysql_port = settings.get('MYSQL_PORT', 3306)
        database = 'news'
        self.db = pymysql.connect(host, mysql_user, mysql_pwd, database, mysql_port)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        sql = """INSERT INTO
                        `cpd_news`(`id`, `url`, `title`, `content`, `category`, `source`, `date`, `news_id`, `page`)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """
        try:
            self.cursor.execute(sql, (
                item.get('id', ''), item.get('url', ''), item.get('title', ''), item.get('content', ''),
                item.get('category', ''),
                item.get('source', ''), item.get('date', ''), item.get('news_id', ''), item.get('page', '')))
            self.db.commit()
        except Exception as e:
            spider.logger.error(f'occur error when db commit date: {e.args[1]}; url: {item.get("url", "")}')
            self.db.rollback()
        return

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()

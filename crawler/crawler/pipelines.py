# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class SavePipeline(object):

    def __init__(self):
        self.f = open('../data/tsv/cpd.tsv', 'a+')

    def process_item(self, item, spider):
        if item.__len__() != 8:
            raise DropItem(item)
            # return
        self.f.write(
            f"{item['news_id']}\t{item['title']}\t{item['category']}\t{item['source']}\t{item['date']}\t{item['page']}\t{item['url']}\t{item['content']}\n")
        return item

    def close_spider(self, spider):
        self.f.close()

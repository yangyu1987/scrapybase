# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import json

class BasetempPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonPipeline(object):

    def process_item(self, item, spider):
        text = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        with open('hc360url.json', 'ab+') as f:
            f.write(text.encode('utf-8'))
        return item


class ImdbMongoPipeline(object):

    def __init__(self,mongo_params):
        # 初始化mongodb信息
        self.client = pymongo.MongoClient('localhost',27017)
        self.db = self.client[mongo_params['db']]

    def process_item(self, item, spider):
        mongo_collection, data = item.mongo_insert()
        collection = self.db[mongo_collection]
        collection.insert(data)
        return item

    @classmethod
    def from_settings(cls,settings):
        mongo_params = {
            'db':settings['MONGO_DB'],
            'collection':settings['MONGO_COLLECTION'],
        }
        return cls(mongo_params)


class MongoPipeline(object):

    def __init__(self,mongo_params):
        # 初始化mongodb信息
        self.client = pymongo.MongoClient('localhost',27017)
        self.db = self.client[mongo_params['db']]

    def process_item(self, item, spider):
        mongo_collection, data = item.mongo_insert()
        collection = self.db[mongo_collection]
        collection.insert(data)
        return item


    @classmethod
    def from_settings(cls,settings):
        mongo_params = {
            'db':settings['MONGO_DB'],
            'collection':settings['MONGO_COLLECTION'],
        }
        return cls(mongo_params)



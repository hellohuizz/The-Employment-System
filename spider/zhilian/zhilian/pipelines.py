# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


# class ZhilianPipeline(object):
#
#     def open_spider(self, spider):
#
#         self.fp = open('beijing.txt','w',encoding='utf8')
#
#
#     def close_spider(self, spider):
#         self.fp.close()
#
#     def process_item(self, item, spider):
#         dic = dict(item)
#         string = json.dumps(dic, ensure_ascii=False)
#         self.fp.write(string + '\n')
#         return item

import pymongo
class MongoDBPipeline(object):
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(host='localhost',port=27017)

    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        dic = dict(item)
        db = self.client.zhilian
        city = dic['city_name']
        col = db.list_collection_names()
        if city in col:
            result = db[city].find({'hash_id': dic['hash_id']}).count()
            if result > 0:
                pass
            else:
                db[city].insert(dic)
        else:
            col = db[city]
            col.insert(dic)

        return item
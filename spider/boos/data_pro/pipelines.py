# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#
# class DataProPipeline(object):
#     def process_item(self, item, spider):
#         return item


import pymongo


class MongoDBPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host='localhost', port=27017)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        dic = dict(item)
        # 先获取城市
        city = dic['item_meta']
        # 从原字典弹出
        dic.pop('item_meta')
        db = self.client.boos
        col = db.list_collection_names()
        # 判断该集合是否存在
        if city in col:  # 集合存在
            result = db[city].find({"hash_id": dic["hash_id"]}).count()
            if result > 0:
                pass
            else:
                db[city].insert(dic)
        else:  # 集合不存在
            # 根据城市建表
            col = db[city]
            col.insert(dic)

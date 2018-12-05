from pymongo import MongoClient

class ConMongodb:
    def __init__(self):
        self.conn = MongoClient('127.0.0.1',27017)

    def con_collection(self,database,collection):
        # 连接数据库
        db = self.conn[database]
        # 连接集合
        self.collection = db[collection]

    def read_data(self):
        #返回全部数据
        return self.collection.find()



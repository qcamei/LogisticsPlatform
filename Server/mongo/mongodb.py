import json
import pymongo
from bson import json_util
from bson.objectid import ObjectId

class MongoDB():
    DB_HOST = "spider"
    DATABASE = "demo"
    COLLECTION = "supply"
    
    def __init__(self):
        client = pymongo.MongoClient(self.DB_HOST)
        database = client[self.DATABASE]
        self.collection = database[self.COLLECTION]

    def insert(self, data):
        self.collection.insert(data) 

    def find(self, obj):
        return self.collection.find(obj)

    def find_one(self, obj):
        return self.collection.find_one(obj)

    def remove(self, obj):
        return self.collection.remove(obj)

    def latest(self):
        return self.find_descending(None)

    def previous(self, obj_id):
        obj = {"_id": {"$lt": ObjectId(obj_id)}}
        return self.find_descending(obj)

    def newer(self, obj_id):
        obj = {"_id": {"$gt": ObjectId(obj_id)}}
        return self.find(obj)

    def find_descending(self, obj = None, count = 10):
        data = []
        top = self.find(obj).sort("_id", pymongo.DESCENDING).limit(count)
        for item in top:
            data.append(item)
        return json.dumps(data, default = json_util.default)
from django.conf import settings
from pymongo import MongoClient
from bson.objectid import ObjectId


class MongoModel:
    client = None
    db = None
    _collection = None
    _instance = None
    _count = 0

    def __init__(self, col_name: str, pk: str = None) -> None:
        self.client = MongoClient(
            host=settings.MONGO_DB.get('host'),
            port=settings.MONGO_DB.get('port'),
            username=settings.MONGO_DB.get('username'),
            password=settings.MONGO_DB.get('password'),
            authSource=settings.MONGO_DB.get('authSource'),
            authMechanism=settings.MONGO_DB.get('authMechanism'),
        )
        self.db = self.client[settings.MONGO_DB.get('name')]
        self._collection = self.db[col_name]

        if pk:
            return self.get(pk)

        return self

    def create(self, **kwargs):
        pk = self._collection.insert_one(kwargs).inserted_id
        return self.get(pk)

    def get(self, pk=None):
        self._instance = self._collection.find_one({'_id': ObjectId(pk)})
        self.__dict__.update(self._instance)
        return self

    def find(self, params: dict = {}, **kwargs):
        self.count(params)
        return self._collection.find(params)

    def count(self, params: dict = {}):
        self._count = self._collection.count_documents(params)
        return self._count

    def save(self):
        values = {}
        for (key, value) in self._instance.items():
            values[key] = getattr(self, key)
        
        self._collection.update(self._instance, values)
        return self

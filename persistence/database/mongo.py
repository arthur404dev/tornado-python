from logzero import logger
from pymongo import MongoClient
from bson.json_util import dumps, ObjectId

import config.settings as settings
import json

_client = None


class MongoDB:
    database_collection: None

    def __init__(self):
        self.get_client()

    def get_client(self, new=False):
        global _client
        try:
            if new or not _client:
                _client = MongoClient(settings.MONGO_URI)
                self.database_collection = _client.get_database(
                    settings.METRICAS_DATABASE)
        except Exception as err:
            logger.error(err)
            _client = None
        return _client

    def set_collection(self, database, collection):
        self.database_collection = _client.get_database(
            name=database).get_collection(name=collection)

    def insert_one(self, data: dict):
        try:
            res = self.database_collection.insert_one(data)
        except Exception as err:
            raise err
        else:
            return str(res.inserted_id)

    def fetch_all(self):
        try:
            res = self.database_collection.find()
        except Exception as err:
            raise err
        else:
            return list(json.loads(dumps(res)))

    def fetch_one(self, doc_id: str):
        try:
            res = self.database_collection.find_one({'_id': ObjectId(doc_id)})
        except Exception as err:
            raise err
        else:
            if res is not None:
                return dict(json.loads(dumps(res)))
            else:
                raise ValueError

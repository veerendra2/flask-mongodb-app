'''
Author: Veerendra Kakumanu
Description: Database Connection
'''
from pymongo import MongoClient
from pymongo import errors
import os
import sys
import json

try:
    USERNAME = os.environ["MONGO_INITDB_ROOT_USERNAME"].strip()
    PASSWORD = os.environ["MONGO_INITDB_ROOT_PASSWORD"].strip()
    MONGODB_HOST = os.environ["MONGODB_SERVICE_SERVICE_HOST"].strip()
    MONGODB_PORT = os.environ["MONGODB_SERVICE_SERVICE_PORT"].strip()
except KeyError:
    sys.stderr.write("[-] 'USERNAME' & 'PASSWORD' environmental variable not set\n")
    exit(1)
DATABASE_NAME = "nova"
COLLECTION_NAME = "config"


class Database:
    def __init__(self):
        self.connect_url = "mongodb://{}:{}@{}:{}/".format(USERNAME, PASSWORD, MONGODB_HOST, MONGODB_PORT)
        self.client = None

    def connect(self):
        try:
            self.client = MongoClient(self.connect_url)
            self.client = self.client[DATABASE_NAME]  # Selecting DB
            self.client = self.client[COLLECTION_NAME]  # Selecting Collection
            return [True, "Success"]
        except errors.ServerSelectionTimeoutError:
            return [False, "Failed to Connect DB"]
        except errors.ConfigurationError:
            return [False, "Configurarion Error"]
        except errors.ConnectionFailure:
            return [False, "Connection Failure"]

    def list_documents(self):
        try:
            cursor = self.client.find({}, {'_id': False})
            return [True, "Success", cursor]
        except Exception:
            return [False, "Internal Error"]

    def create_document(self, document):
        try:
            self.client.insert_one(document)
            return [True, "Success"]
        except errors.DuplicateKeyError:
            return [False, "The config name is already exist"]

    def get_document(self, doc):
        try:
            cursor = self.client.find_one({"name": doc}, {'_id': False})
            if cursor is not None:
                return [True, "Success", cursor]
            else:
                return [False, "No document found"]
        except Exception as e:
            return [False, "Internal Error"]

    def update_document(self, config_name, data):
        try:
            result = self.client.replace_one({"name": config_name}, {"name": config_name, "data": data})
            if result.acknowledged:
                return [True, "Success", result]
            else:
                raise Exception
        except Exception:
            return [False, "Internal Error"]

    def purge_document(self, document):
        try:
            cursor = self.client.delete_one({"name": document})
            return [True, "Success", cursor.deleted_count]
        except Exception:
            return [False, "Internal Error"]

    def query(self, key, val, config_name=None):
        if config_name is None:
            query = '[{{"$match": {{}}}}, {{"$unwind":"$data"}}, {{"$match":{{"data.{0}": "{1}"}}}}]'
            replaced_query = json.loads(query.format(key, val))
        else:
            query = '[{{"$match": {{"name": "{0}"}}}}, {{"$unwind":"$data"}}, {{"$match":{{"data.{1}": "{2}"}}}}]'
            replaced_query = json.loads(query.format(config_name, key, val))
        try:
            cursor = self.client.aggregate(replaced_query)
            if cursor is not None:
                return [True, "Success", cursor]
            else:
                return [False, "No document found"]
        except Exception as e:
            return [False, str(e)]


if __name__ == '__main__':
    pass

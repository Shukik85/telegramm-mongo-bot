'''
Используйте MongoClient для создания соединения.
MongoClient по умолчанию использует экземпляр MongoDB,
запущенный на localhost:27017 если не указан.
'''

import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
import bson


load_dotenv()
URI = os.getenv("DB_URL")
PATH = os.getenv("DB_BACKUP_DIR")
DB = os.getenv("DB_DATABASE")

client = MongoClient(URI)
db = client.DB
path_coll = os.path.join(PATH, DB)


def get_data_to_db(dct):
    dt_from = datetime.fromisoformat(dct["dt_from"])
    dt_upto = datetime.fromisoformat(dct["dt_upto"])
    group_type = dct["group_type"]
    collections = db.sample_collection
    pipeline = [
        {
            "$match": {
                "$or": [
                    {
                        "dt": {
                            "$gte": dt_from,
                            "$lte": dt_upto
                        }
                    },
                ]
            }
        },
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "date": {
                            "$dateTrunc": {
                                "date": "$dt", "unit": group_type, "binSize": 1
                            }
                        }
                    }
                },
                "values": {"$sum": "$value"}
            }
        },
        {"$sort": {"_id": 1}},
        {
            "$group": {
                "_id": "null",
                "dataset": {
                    "$push": "$values"
                },
                "labels": {
                    "$push": "$_id"
                }
            }
        },
        {"$project": {"_id": 0}}
    ]
    print(pipeline)
    collection = None
    with client.start_session(snapshot=True) as session:
        collection = collections.aggregate(
            pipeline=pipeline, session=session).try_next()
    return collection


def restore():
    """
    MongoDB Restore

    :param path: Database dumped path
    :param client: MongoDB client clientection
    :param db_name: Database name
    :return:

    >>> DB_BACKUP_DIR = '/path/backups/'
    >>> client = MongoClient("mongodb://admin:admin@127.0.0.1:27017", authSource="admin")
    >>> db_name = 'my_db'
    >>> restore(DB_BACKUP_DIR, client, db_name)

    """
    for coll in os.listdir(path=path_coll):
        if coll.endswith('.bson'):
            with open(os.path.join(path_coll, coll), 'rb+') as f:
                try:
                    db[coll.split('.')[0]].insert_many(
                        bson.decode_all(f.read()))
                    print("Ok!")
                except BulkWriteError:
                    pass


# def dump(collections, client, db_name, path):
#     """
#     MongoDB Dump

#     :param collections: Database collections name
#     :param client: MongoDB client clientection
#     :param db_name: Database name
#     :param path:
#     :return:

#     >>> DB_BACKUP_DIR = '/path/backups/'
#     >>> client = MongoClient("mongodb://admin:admin@127.0.0.1:27017", authSource="admin")
#     >>> db_name = 'my_db'
#     >>> collections = ['collection_name', 'collection_name1', 'collection_name2']
#     >>> dump(collections, client, db_name, DB_BACKUP_DIR)
#     """

#     db = client[db_name]
#     for coll in collections:
#         with open(os.path.join(path, f'{coll}.bson'), 'wb+') as f:
#             for doc in db[coll].find():
#                 f.write(bson.BSON.encode(doc))

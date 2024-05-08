import dataclasses
from dataclasses import dataclass
from typing import Optional

from utils.mongo_store_broker import mongo
from bson.objectid import ObjectId


@dataclass
class Notification:
    text: str
    user_id: ObjectId
    _id: Optional[ObjectId] = ObjectId()

    def get_id(self):
        return self._id

    def __iter__(self):
        for field in dataclasses.fields(self):
            yield field.name, getattr(self, field.name)


class Dao:

    @staticmethod
    def find_one(_id: str | ObjectId):
        if isinstance(_id, str):
            _id = ObjectId(_id)
        res = mongo.db.notifications.find_one({"_id": _id})
        return Notification(**res)

    @staticmethod
    def insert_one(obj: dict | Notification):
        return mongo.db.notifications.insert_one(dict(obj)).inserted_id

    @staticmethod
    def update_one(_id: str | ObjectId, obj: Notification):
        if isinstance(_id, str):
            _id = ObjectId(_id)
        return mongo.db.notifications.update_one({"_id": _id},
                                                 {"$set": dict(obj)})

    @staticmethod
    def delete_one(_id: str | ObjectId):
        if isinstance(_id, str):
            _id = ObjectId(_id)
        return mongo.db.notifications.delete_one({"_id": _id})

    @staticmethod
    def get_all():
        res = mongo.db.notifications.find({})
        return [Notification(**r) for r in res]

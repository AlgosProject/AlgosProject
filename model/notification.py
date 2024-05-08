import dataclasses
from dataclasses import dataclass
from typing import Optional

from utils.mongo_store_broker import mongo
from bson.objectid import ObjectId


@dataclass  # Autogenerates __init__, __eq___ and __repr__ from given fields
class Notification:
    text: str
    user_id: ObjectId
    _id: Optional[ObjectId] = ObjectId()

    def get_id(self):  # in python _ before a field indicates that its protected so a method is used to retrive it
        return self._id

    def __iter__(self):  # This method allows us to add support for dict() on an object
        for field in dataclasses.fields(self):
            yield field.name, getattr(self, field.name)


class Dao:

    @staticmethod
    def find_one(_id: str | ObjectId):
        """
        Returns a notification object from db
        :param _id:
        :return:
        """
        if isinstance(_id, str):
            _id = ObjectId(_id)
        res = mongo.db.notifications.find_one({"_id": _id})
        return Notification(**res)

    @staticmethod
    def insert_one(obj: dict | Notification):
        """
        Inserts one notification object into the db
        :param obj:
        :return:
        """
        return mongo.db.notifications.insert_one(dict(obj)).inserted_id

    @staticmethod
    def update_one(_id: str | ObjectId, obj: Notification):
        """
        Updates a notification object inside the db
        :param _id:
        :param obj:
        :return:
        """
        if isinstance(_id, str):
            _id = ObjectId(_id)
        return mongo.db.notifications.update_one({"_id": _id},
                                                 {"$set": dict(obj)})

    @staticmethod
    def delete_one(_id: str | ObjectId):
        """
        Deletes a notification object inside the db
        :param _id:
        :return:
        """
        if isinstance(_id, str):
            _id = ObjectId(_id)
        return mongo.db.notifications.delete_one({"_id": _id})

    @staticmethod
    def get_all():
        """
        :return: - A list of Notification objects
        """
        res = mongo.db.notifications.find({})
        return [Notification(**r) for r in res]

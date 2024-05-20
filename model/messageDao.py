import dataclasses
from dataclasses import dataclass
from typing import Optional

from utils.mongo_store_broker import mongo
from bson.objectid import ObjectId
import model.userDao

@dataclass  # Autogenerated __init__, __eq___ and __repr__ from given fields
class Message:
    text: str
    user_id: ObjectId
    group_id: ObjectId
    _id: Optional[ObjectId] = dataclasses.field(default_factory=ObjectId)

    @property
    def id(self):
        return self._id

    @property
    def author(self):
        return model.userDao.find_one(self.user_id)

    def __iter__(self):  # This method allows us to add support for dict() on an object
        for field in dataclasses.fields(self):
            yield field.name, getattr(self, field.name)


def find_one(_id: str | ObjectId):
    """
    Returns a notification object from db
    :param _id:
    :return:
    """
    if isinstance(_id, str):
        _id = ObjectId(_id)
    res = mongo.db.messages.find_one({"_id": _id})
    if res:
        return Message(**res)


def find_all_messages_from_group(_id):
    if isinstance(_id, str):
        _id = ObjectId(_id)
    res = mongo.db.messages.find({"group_id": _id})
    return [Message(**r) for r in res]

def insert_one(obj: dict | Message):
    """
    Inserts one notification object into the db
    :param obj:
    :return:
    """
    return mongo.db.messages.insert_one(dict(obj)).inserted_id


def update_one(_id: str | ObjectId, obj: Message):
    """
    Updates a notification object inside the db
    :param _id:
    :param obj:
    :return:
    """
    if isinstance(_id, str):
        _id = ObjectId(_id)
    return mongo.db.messages.update_one({"_id": _id},
                                        {"$set": dict(obj)})


def delete_one(_id: str | ObjectId):
    """
    Deletes a notification object inside the db
    :param _id:
    :return:
    """
    if isinstance(_id, str):
        _id = ObjectId(_id)
    return mongo.db.messages.delete_one({"_id": _id})


def get_all():
    """
    :return: - A list of Notification objects
    """
    res = mongo.db.messages.find({})
    return [Message(**r) for r in res]

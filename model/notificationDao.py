import dataclasses
from dataclasses import dataclass
from typing import Optional

from utils.mongo_store_broker import mongo
from bson.objectid import ObjectId
import model.userDao


@dataclass  # Autogenerated __init__, __eq___ and __repr__ from given fields
class Notification:
    user_id: ObjectId
    author_id: ObjectId
    origin_id: ObjectId
    type: str
    _id: Optional[ObjectId] = dataclasses.field(default_factory=ObjectId)

    @property
    def id(self):
        return self._id

    @property
    def for_user(self):
        return model.userDao.find_one(self.user_id)

    @property
    def author(self):
        return model.userDao.find_one(self.author_id)

    @property
    def is_chat(self):
        return self.type == "chat"

    @property
    def is_friend_request(self):
        return self.type == "friend_request"

    @property
    def text(self):
        notif_str = ""
        if self.is_chat:
            notif_str = f"There is a message waiting for you from {self.author.name}"
        if self.is_friend_request:
            notif_str = f"You got a friend request from {self.author.name}"
        return notif_str

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
    res = mongo.db.notifications.find_one({"_id": _id})
    if res:
        return Notification(**res)


def find_one_by_origin_id_author_id(origin_id: str | ObjectId, author_id: str | ObjectId):
    """
    Returns a notification object from db
    :param author_id:
    :param origin_id:
    :return:
    """
    if isinstance(origin_id, str):
        origin_id = ObjectId(origin_id)
    if isinstance(author_id, str):
        author_id = ObjectId(author_id)
    res = mongo.db.notifications.find({"origin_id": origin_id, "author_id": author_id})
    return [Notification(**r) for r in res]


def find_by_user_id_and_author_id(_id: str | ObjectId, author_id: str | ObjectId):
    """
    :return: - A list of Notification objects
    """
    if isinstance(_id, str):
        _id = ObjectId(_id)
    if isinstance(author_id, str):
        author_id = ObjectId(author_id)
    res = mongo.db.notifications.find({"user_id": _id, "author_id": author_id})
    return [Notification(**r) for r in res]


def find_fr_by_author_id(author_id: str | ObjectId):
    """
    :return: - A list of Notification objects
    """

    if isinstance(author_id, str):
        author_id = ObjectId(author_id)
    res = mongo.db.notifications.find({"type": "friend_request", "author_id": author_id})
    return [Notification(**r) for r in res]


def find_by_user_id(_id: str | ObjectId):
    """
    :return: - A list of Notification objects
    """
    if isinstance(_id, str):
        _id = ObjectId(_id)
    res = mongo.db.notifications.find({"user_id": _id})
    return [Notification(**r) for r in res]


def find_by_user_id_type(_id, type_):
    """
    :return: - A list of Notification objects
    """
    if isinstance(_id, str):
        _id = ObjectId(_id)
    res = mongo.db.notifications.find({"user_id": _id, "type": type_})
    return [Notification(**r) for r in res]


def insert_one(obj: dict | Notification):
    """
    Inserts one notification object into the db
    :param obj:
    :return:
    """
    return mongo.db.notifications.insert_one(dict(obj)).inserted_id


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


def delete_one(_id: str | ObjectId):
    """
    Deletes a notification object inside the db
    :param _id:
    :return:
    """
    if isinstance(_id, str):
        _id = ObjectId(_id)
    return mongo.db.notifications.delete_one({"_id": _id})


def get_all():
    """
    :return: - A list of Notification objects
    """
    res = mongo.db.notifications.find({})
    return [Notification(**r) for r in res]

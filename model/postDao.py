import dataclasses
from dataclasses import dataclass
from typing import Optional
from utils.mongo_store_broker import mongo
from bson.objectid import ObjectId
import model.userDao


@dataclass  # Autogenerated __init__, __eq___ and __repr__ from given fields
class Post:
    likes: list[ObjectId]
    photo_url: str
    tags: list[ObjectId]
    text: str
    user_id: ObjectId
    comments: list[ObjectId]
    _id: Optional[ObjectId] = dataclasses.field(default_factory=ObjectId)

    def __iter__(self):  # This method allows us to add support for dict() on an object
        for field in dataclasses.fields(self):
            yield field.name, getattr(self, field.name)

    @property
    def id(self):
        return self._id

    @property
    def likes_amount(self):
        return len(self.likes)

    @property
    def user(self):
        return model.userDao.find_one(self.user_id)


def find_one(_id: str | ObjectId):
    """
    Returns a Post object from db
    :param _id:
    :return:
    """
    if isinstance(_id, str):
        _id = ObjectId(_id)
    res = mongo.db.posts.find_one({"_id": _id})
    if res:
        return Post(**res)


def find_posts_by_user(_id: str | ObjectId):
    """
        :return: - A list of Post objects from a specific user
    """
    if isinstance(_id, str):
        _id = ObjectId(_id)
    res = mongo.db.posts.find({"user_id": _id})
    return [Post(**r) for r in res]


def find_posts_by_tag(_id: str | ObjectId):
    """
        :return: - A list of Post objects with a specific user
    """
    if isinstance(_id, str):
        _id = ObjectId(_id)
    res = mongo.db.posts.find({"tags": _id})
    return [Post(**r) for r in res]


def insert_one(obj: dict | Post):
    """
    Inserts one Post object into the db
    :param obj:
    :return:
    """
    return mongo.db.posts.insert_one(dict(obj)).inserted_id


def update_one(_id: str | ObjectId, obj: Post):
    """
    Updates a Post object inside the db
    :param _id:
    :param obj:
    :return:
    """
    if isinstance(_id, str):
        _id = ObjectId(_id)
    return mongo.db.posts.update_one({"_id": _id},
                                     {"$set": dict(obj)})


def delete_one(_id: str | ObjectId):
    """
    Deletes a Post object inside the db
    :param _id:
    :return:
    """
    if isinstance(_id, str):
        _id = ObjectId(_id)
    return mongo.db.posts.delete_one({"_id": _id})


def get_all():
    """
    :return: - A list of Post objects
    """
    res = mongo.db.posts.find({})
    return [Post(**r) for r in res]

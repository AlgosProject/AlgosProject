import dataclasses
from dataclasses import dataclass
from typing import Optional

from utils.mongo_store_broker import mongo
from bson.objectid import ObjectId


@dataclass  # Autogenerated __init__, __eq___ and __repr__ from given fields
class User:
    friends: dict
    name: str
    privacy_control: int
    username: str
    password: str
    tags: dict
    seen: list[ObjectId]
    _id: Optional[ObjectId] = ObjectId()

    def get_id(self):  # in python _ before a field indicates that its protected so a method is used to retrieve it
        return self._id

    def __iter__(self):  # This method allows us to add support for dict() on an object
        for field in dataclasses.fields(self):
            yield field.name, getattr(self, field.name)


class Dao:

    @staticmethod
    def find_one(_id: str | ObjectId):
        """
        Returns a user object from db
        :param _id:
        :return:
        """
        if isinstance(_id, str):
            _id = ObjectId(_id)
        res = mongo.db.users.find_one({"_id": _id})
        return User(**res)

    @staticmethod
    def insert_one(obj: dict | User):
        """
        Inserts one user object into the db
        :param obj:
        :return:
        """
        return mongo.db.users.insert_one(dict(obj)).inserted_id

    @staticmethod
    def update_one(_id: str | ObjectId, obj: User):
        """
        Updates a user object inside the db
        :param _id:
        :param obj:
        :return:
        """
        if isinstance(_id, str):
            _id = ObjectId(_id)
        return mongo.db.users.update_one({"_id": _id},
                                            {"$set": dict(obj)})

    @staticmethod
    def delete_one(_id: str | ObjectId):
        """
        Deletes a user object inside the db
        :param _id:
        :return:
        """
        if isinstance(_id, str):
            _id = ObjectId(_id)
        return mongo.db.users.delete_one({"_id": _id})

    @staticmethod
    def get_all():
        """
        :return: - A list of user objects
        """
        res = mongo.db.users.find({})
        return [User(**r) for r in res]

import dataclasses
from collections import deque
from dataclasses import dataclass
from typing import Optional

from flask import current_app
from flask_bcrypt import Bcrypt

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
    _id: Optional[ObjectId] = dataclasses.field(default_factory=ObjectId)

    def get_id(self):  # in python _ before a field indicates that its protected so a method is used to retrieve it
        return self._id

    def __iter__(self):  # This method allows us to add support for dict() on an object
        for field in dataclasses.fields(self):
            yield field.name, getattr(self, field.name)

    def get_friends_dict(self):
        friends_dict = dict()
        for f in self.friends:
            friends_dict[f['friend_id']] = f['affinity']
        return friends_dict

    def bfs_get_visible_user_ids(self):
        current_lvl = deque()  # Current level
        current_lvl.append(self.get_id())
        next_lvl = deque()  # Next level
        visited = [self.get_id()]  # Visited nodes/users
        distance = 1  # Distance from start level

        while len(current_lvl) != 0:
            while len(current_lvl) != 0:
                current = current_lvl.popleft()
                neighbours = find_one(current).get_friends_dict().keys()

                for n in neighbours:
                    # Filtering criteria
                    # If node within reach of your privacy control
                    distance_within_privacy = distance <= self.privacy_control
                    # If other node has a higher privacy than self
                    ns_privacy_control = find_one(n).privacy_control >= self.privacy_control

                    # Visit node
                    if n not in visited and distance_within_privacy and ns_privacy_control:
                        next_lvl.append(n)
                        visited.append(n)

            distance += 1
            current_lvl = next_lvl
            next_lvl = deque()

        return visited


def find_one(_id: str | ObjectId):
    """
    Returns a user object from db
    :param _id:
    :return:
    """
    if isinstance(_id, str):
        _id = ObjectId(_id)
    res = mongo.db.users.find_one({"_id": _id})
    if res:
        return User(**res)


def find_user_by_username(username: str):
    res = mongo.db.users.find_one({"username": username})
    if res:
        return User(**res)


def find_user_by_id(_id: str | ObjectId):
    if isinstance(_id, str):
        _id = ObjectId(_id)
    res = mongo.db.users.find_one({"_id": _id})
    if res:
        return User(**res)


def insert_one(obj: dict | User):
    """
    Inserts one user object into the db
    :param obj:
    :return:
    """
    return mongo.db.users.insert_one(dict(obj)).inserted_id


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


def delete_one(_id: str | ObjectId):
    """
    Deletes a user object inside the db
    :param _id:
    :return:
    """
    if isinstance(_id, str):
        _id = ObjectId(_id)
    return mongo.db.users.delete_one({"_id": _id})


def get_all():
    """
    :return: - A list of user objects
    """
    res = mongo.db.users.find({})
    return [User(**r) for r in res]


def login(username, psw) -> User:
    bcrypt: Bcrypt = current_app.bcrypt

    user = find_user_by_username(username)

    if user:
        if bcrypt.check_password_hash(user.password, psw):
            return user

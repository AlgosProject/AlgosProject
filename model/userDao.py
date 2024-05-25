import dataclasses
from math import log
from collections import deque
from dataclasses import dataclass
from typing import Optional, List, Dict, Set
from flask import current_app
from flask_bcrypt import Bcrypt

import model.tagDao
from utils.mongo_store_broker import mongo
from bson.objectid import ObjectId


@dataclass  # Autogenerated __init__, __eq___ and __repr__ from given fields
class User:
    friends: dict
    name: str
    privacy_control: int
    username: str
    password: str
    tags: List[Dict[str, int]]
    seen: Set[ObjectId]
    photo_url: Optional[str] = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
    _id: Optional[ObjectId] = dataclasses.field(default_factory=ObjectId)

    def __post_init__(self):
        self.seen = set(self.seen)

    @property
    def id(self):
        return self._id

    @property
    def tags_built(self):
        tags = []
        for tag in self.tags:
            t = dict()
            t["tag"] = model.tagDao.find_one(tag['tag_id'])
            t["affinity"] = tag['affinity']
            tags.append(t)
        return tags

    def __iter__(self):  # This method allows us to add support for dict() on an object
        for field in dataclasses.fields(self):
            yield field.name, getattr(self, field.name)

    def get_friends_dict(self):
        friends_dict = dict()
        for f in self.friends:
            friends_dict[f['friend_id']] = f['affinity']
        return friends_dict

    def bfs_get_visible_user_ids(self):
        """
        Gets all the visible user ids of this user given its privacy setting
        :return:
        """
        current_lvl = deque()  # Current level
        current_lvl.append(self.id)
        next_lvl = deque()  # Next level
        visited = [self.id]  # Visited nodes/users
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

    def get_user_tags_ordered_by_affinity(self):
        tags = self.tags_built
        tags.sort(key=lambda x: x.get("affinity"))
        return tags

    def leave_tag(self, _id):
        for t in self.tags:
            if t["tag_id"] == ObjectId(_id):
                t["affinity"] = -5
                update_one(self.id, self)

    def joint_tag(self, tag_id):
        t = dict()
        if tag_id not in [u_tag["tag_id"] for u_tag in self.tags]:
            t["tag_id"] = ObjectId(tag_id)
            t["affinity"] = 1
            self.tags.append(t)
        else:
            for t in self.tags:
                if t["tag_id"] == ObjectId(tag_id):
                    t["affinity"] = 1

        update_one(self.id, self)

    def see_message(self, _id):
        print(type(self.seen))
        self.seen.add(_id)
        update_one(self.id, self)
        return self


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


def find__positive_affinity_user_by_tag_id(_id: str | ObjectId):
    if isinstance(_id, str):
        _id = ObjectId(_id)
    res = mongo.db.users.find(
        {"tags": {"$elemMatch": {"tag_id": _id, "affinity": {"$gt": 0}}}}
    )
    return [User(**r) for r in res]


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
    new_obj = {k: v for (k, v) in zip(dict(obj).keys(), dict(obj).values())}

    if isinstance(_id, str):
        _id = ObjectId(_id)

    if isinstance(new_obj["seen"], set):
        new_obj["seen"] = list(new_obj["seen"])

    return mongo.db.users.update_one({"_id": _id},
                                     {"$set": dict(new_obj)})


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

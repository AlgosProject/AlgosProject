import dataclasses
from dataclasses import dataclass
from typing import Optional
from utils.mongo_store_broker import mongo
from bson.objectid import ObjectId
import model.userDao
import re


@dataclass  # Autogenerated __init__, __eq___ and __repr__ from given fields
class Post:
    likes: list[ObjectId]
    dislikes: list[ObjectId]
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
    def dislikes_amount(self):
        return len(self.dislikes)

    @property
    def user(self):
        return model.userDao.find_one(self.user_id)

    @property
    def like_weight(self):
        return 1

    @property
    def dislike_weight(self):
        return -3

    def like_post(self, user: model.userDao.User):
        if user.id not in self.likes:
            self.likes.append(user.id)

            user = user.change_tag_affinity(self.tags, self.like_weight)

            if user.id in self.dislikes:
                self.dislikes.remove(user.id)
                user = user.change_tag_affinity(self.tags, -self.dislike_weight)

        elif user.id in self.likes:
            self.likes.remove(user.id)
            user = user.change_tag_affinity(self.tags, -self.like_weight)

        update_one(self.id, self)
        return user

    def dislike_post(self, user: model.userDao):
        if user.id not in self.dislikes:
            self.dislikes.append(user.id)
            user = user.change_tag_affinity(self.tags, self.dislike_weight)

            if user.id in self.likes:
                self.likes.remove(user.id)
                user = user.change_tag_affinity(self.tags, -self.like_weight)

        elif user.id in self.dislikes:
            self.dislikes.remove(user.id)
            user = user.change_tag_affinity(self.tags, -self.dislike_weight)

        update_one(self.id, self)
        return user


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


def get_all_like(pattern: str):
    """
    :return: - A list of Post objects that satisfy the pattern
    """
    regx = re.compile(".*" + pattern + ".*", re.IGNORECASE)
    search = {
        "text": regx
    }
    res = mongo.db.posts.find(search)
    posts = [Post(**r) for r in res]
    object_id_set = {r['_id'] for r in res}
    commentlist = mongo.db.comments.find(search)
    for comment in commentlist:
        if comment['post_id'] not in object_id_set:
            post = find_one(comment['post_id'])
            posts.append(post)
            object_id_set.add(post.id)
    return posts

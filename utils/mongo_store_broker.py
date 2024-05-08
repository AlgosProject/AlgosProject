from flask_pymongo import PyMongo

mongo = PyMongo()


def find_one(collection, obj_id):
    """
    Returns a dictionary with the same id from the collection
    :param collection:
    :param obj_id:
    :return:
    """
    return mongo.db[collection].find_one(obj_id)


def insert_one(collection, obj):
    """
    Insert into collection the object and return its id
    :param collection:
    :param obj:
    :return:
    """
    return mongo.db[collection].insert_one(obj).inserted_id


def update_one(collection, obj_id, obj):
    return mongo.db[collection].update_one({"_id": obj_id},
                                           {"$set": obj})


def delete_one(collection, obj_id):
    return mongo.db[collection].delete_one({"_id": obj_id})

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




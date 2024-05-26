from flask import Blueprint, jsonify, request, session, flash

from model import userDao, notificationDao

add_friend_blueprint = Blueprint("add_friend", __name__, template_folder="templates")


@add_friend_blueprint.route("/add_friend_to_user", methods=["POST"])
def add_friend():  # put application's code here
    user = session["user"]
    user = userDao.User(**user)
    friendid = request.form.get("friendId")
    action = request.form.get("type")
    if action == "add":
        notificationDao.insert_one(
            {
                "user_id": friendid,
                "type": "friend_request",
                "author_id": user.id,
            }
        )
        return jsonify(success=1, message="Request sent successfully")

    elif action == "delete":
        session["user"] = dict(user.delete_friend(friendid))
        return jsonify(success=1, message="Deleted successfully")

    return jsonify(success=0, message="Something went wrong")

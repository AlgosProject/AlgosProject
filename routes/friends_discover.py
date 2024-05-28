from bson import ObjectId
from flask import Blueprint, render_template, session, request, redirect, url_for

from model import notificationDao, userDao
from utils import check_logged_in

friendsDiscover_blueprint = Blueprint("friends_discover", __name__, template_folder="templates")


@friendsDiscover_blueprint.route("/friends_discover", methods=["GET", "POST"])
def friends_discover():
    status = check_logged_in.check_session()
    if status:
        return status
    user = userDao.User(**session["user"])
    received_friend_requests = [f.author for f in user.fr_notifications if f.author_id != user.id]
    sent_friend_requests = [f.user_id for f in notificationDao.find_fr_by_author_id(user.id)]

    if request.method == "GET":
        common_friends = dict()
        notifs = dict()

        for u in received_friend_requests:
            common_friends[u.id] = len(user.get_common_friends(u.id))

        for n in user.fr_notifications:
            notifs[n.author_id] = n.id

        visible_user = user.bfs_get_visible_user_ids()
        visible_user.sort(key=lambda other_id: user.compare_affinity(other_id))

        for u_id in visible_user:
            if u_id not in common_friends.keys():
                common_friends[u_id] = len(user.get_common_friends(u_id))

        suggestions = [userDao.find_one(u) for u in visible_user
                       if u != user.id and u not in [u["friend_id"] for u in user.friends]]

        return render_template("friends_discover.jinja2",
                               pending_fr=received_friend_requests,
                               common_friends=common_friends,
                               notifs=notifs,
                               empty_fr=not bool(len(received_friend_requests)),
                               suggestions=suggestions,
                               sent_fr=sent_friend_requests,
                               user=user
                               )

    if request.method == "POST":
        if request.form["action"] == "friend_request":
            if notificationDao.find_by_user_id_and_author_id(ObjectId(request.form["friend_id"]), user.id):
                return redirect(url_for("friends_discover.friends_discover"))

            else:
                notificationDao.insert_one({
                    "user_id": ObjectId(request.form["friend_id"]),
                    "origin_id": None,
                    "type": "friend_request",
                    "author_id": user.id,
                })
                return redirect(url_for("friends_discover.friends_discover"))

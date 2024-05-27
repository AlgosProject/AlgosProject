from flask import Blueprint, render_template, session, request, redirect, url_for

from model import userDao

from model import notificationDao
from utils import check_logged_in

notification_blueprint = Blueprint("notification", __name__, template_folder="templates")


@notification_blueprint.route("/notification", methods=["GET", "POST"])
def notification():
    status = check_logged_in.check_session()
    if status:
        return status
    user = userDao.User(**session["user"])

    if request.method == "GET":
        notifs = user.notifications
        if request.args.get("json"):
            return dict({
                "total": len(notifs),
                "fr_amount": len([n for n in notifs if n.is_friend_request]),
                "chats_amount": len([n for n in notifs if n.is_chat])
            })

        if notifs:
            return render_template('notification.jinja2', notifs=notifs)
        else:
            return render_template('notification.jinja2', empty=True)

    if request.method == "POST":
        notificationDao.delete_one(request.form["notif_id"])
        if request.form["action"] == "open_chat":
            return redirect(url_for("chats.chat", id=request.form["chat_id"]))
        if request.form["action"] == "accept_request":
            friend_id = request.form["friend_id"]
            session["user"] = dict(user.add_friend(friend_id))
            friend = userDao.find_one(friend_id)
            friend.add_friend(user.id)
            return redirect(url_for("notification.notification"))
        if request.form["action"] == "decline_request":
            return redirect(url_for("notification.notification"))

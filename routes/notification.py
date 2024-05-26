from flask import Blueprint, render_template, session, request, redirect, url_for

from model import userDao

from model import notificationDao

notification_blueprint = Blueprint("notification", __name__, template_folder="templates")


@notification_blueprint.route("/notification", methods=["GET", "POST"])
def notification():
    user = userDao.User(**session["user"])

    if request.method == "GET":
        notifs = user.notifications
        if notifs:
            return render_template('notification.jinja2', notifs=notifs)
        else:
            return render_template('notification.jinja2', empty=True)

    if request.method == "POST":
        notificationDao.delete_one(request.form["notif_id"])
        if request.form["action"] == "open_chat":
            return redirect(url_for("chats.chat", id=request.form["chat_id"]))
        if request.form["action"] == "accept_request":
            session["user"] = dict(user.add_friend(request.form["friend_id"]))
            return redirect(url_for("notification.notification"))
        if request.form["action"] == "decline_request":
            return redirect(url_for("notification.notification"))

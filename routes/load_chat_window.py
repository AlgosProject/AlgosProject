from bson import ObjectId
from flask import Blueprint, render_template, session, request, redirect, url_for

from model import groupDao, userDao, messageDao, notificationDao
from utils import check_logged_in

load_chats_blueprint = Blueprint("load_chats", __name__, template_folder="templates")


@load_chats_blueprint.route("/load_chats", methods=["POST"])
def chat():  # put application's code here
    status = check_logged_in.check_session()
    if status:
        return status
    user = userDao.User(**session.get("user"))
    chats = groupDao.find_all_chats_by_user(user.id)
    chat_id = request.json['data']
    notifs = notificationDao.find_by_user_id_type(user.id, "chat")
    if chat_id is None:
        if len(chats) == 0:
            return render_template("chats.jinja2")
        else:
            return redirect(url_for("chats.chat", id=chats.pop().id))
    else:
        curr_messages = messageDao.find_all_messages_from_group(chat_id)

        chats_dest_seen = []
        for c in chats:
            dest = c.users_built
            dest.remove(user)
            seen = c.id not in [n.origin_id for n in notifs]
            chats_dest_seen.append((c, dest.pop(), seen))

        current_recipient = [c[1] for c in chats_dest_seen if str(c[0].id) == chat_id].pop()

        curr_chat_notifs = notificationDao.find_one_by_origin_id_author_id(chat_id, current_recipient.id)

        for notif in curr_chat_notifs:
            notificationDao.delete_one(notif.id)

        return render_template(
            "chat_window.jinja2",
            messages=curr_messages,
            current_uid=user.id,
        )

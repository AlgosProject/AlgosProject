from bson import ObjectId
from flask import Blueprint, render_template, session, request, redirect, url_for

from model import groupDao, userDao, messageDao, notificationDao

chats_blueprint = Blueprint("chats", __name__, template_folder="templates")


@chats_blueprint.route("/chats", methods=["GET", "POST"])
def chat():  # put application's code here
    user = userDao.User(**session.get("user"))
    chats = groupDao.find_all_chats_by_user(user.id)
    chat_id = request.args.get("id")
    notifs = notificationDao.find_by_user_id_type(user.id, "chat")

    if request.method == "GET":
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

            return render_template(
                "chats.jinja2",
                side_items=chats_dest_seen,
                messages=curr_messages,
                current_uid=user.id,
                current_recipient=current_recipient,
                seen=user.seen
            )

    if request.method == "POST":
        if request.form["action"] == "send":
            m_id = messageDao.insert_one(
                {"user_id": user.id, "group_id": ObjectId(chat_id), "text": request.form["message_text"]})
            session["user"] = dict(user)

            return redirect(url_for("chats.chat", id=chat_id))

        elif request.form["action"] == "delete_chat":
            chat_id = request.form["to_delete_group"]
            messageDao.delete_all_messages_group(chat_id)
            groupDao.delete_one(chat_id)
            return redirect(url_for("chats.chat"))

        elif request.form["action"] == "open_chat":
            found_chats = groupDao.find_chat_of_two_users(user.id, request.form["friend_id"])
            if len(found_chats) != 0:
                return redirect(url_for("chats.chat", id=found_chats[0].id))
            else:
                chat_id = groupDao.insert_one({"users": [user.id, request.form["friend_id"]], "type": "chat"})
                return redirect(url_for("chats.chat", id=chat_id))

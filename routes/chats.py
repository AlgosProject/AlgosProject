from bson import ObjectId
from flask import Blueprint, render_template, session, request, redirect, url_for

from model import groupDao, userDao, messageDao

chats_blueprint = Blueprint("chats", __name__, template_folder="templates")


@chats_blueprint.route("/chats", methods=["GET", "POST"])
def chat():  # put application's code here
    user = userDao.User(**session.get("user"))
    chats = groupDao.find_all_chats_by_user(user.id)
    chat_id = request.args.get("id")
    if chat_id is None:
        if len(chats) != 0:
            return redirect(url_for("chats.chat", id=chats.pop().id))
        else:
            pass
        # TODO: What happens if you have no active chats :c

    if request.method == "GET":
        curr_messages = messageDao.find_all_messages_from_group(chat_id)
        chats_dest = []
        for c in chats:
            dest = c.users_built
            dest.remove(user)
            chats_dest.append((c, dest.pop()))

        current_chat_dest = [c[1] for c in chats_dest if str(c[0].id) == chat_id].pop()

        return render_template(
            "chats.jinja2",
            side_items=chats_dest,
            messages=curr_messages,
            current_uid=user.id,
            current_chat_dest=current_chat_dest,
            current_chat_id=chat_id
        )

    if request.method == "POST":
        if request.form["action"] == "send":
            messageDao.insert_one(
                {"user_id": user.id, "group_id": ObjectId(chat_id), "text": request.form["message_text"]})
            return redirect(url_for("chats.chat", id=chat_id))
        elif request.form["action"] == "delete_chat":
            chat_id = request.form["to_delete_group"]

            messageDao.delete_all_messages_group(chat_id)
            groupDao.delete_one(chat_id)
            return redirect(url_for("chats.chat"))

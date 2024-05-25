from bson import ObjectId
from flask import Blueprint, render_template, session, request, redirect, url_for

from model import userDao, postDao, commentDao

popup_blueprint = Blueprint("media_popup", __name__, template_folder="templates")


@popup_blueprint.route("/media", methods=["GET", "POST"])
def popup():
    user = userDao.User(**session.get("user"))
    if request.method == "GET":
        post = postDao.find_one(request.args.get("post_id"))
        comments = commentDao.find_comments_by_post_id(post.id)

        return render_template("media_popup.jinja2", post=post, comments=comments)

    if request.method == "POST":
        if request.form["action"] == "post_comment":
            post_id = ObjectId(request.form["post_id"])

            commentDao.insert_one({"post_id": post_id, "text": request.form["comment_text"], "user_id": user.id})

            return redirect(url_for("media_popup.popup", post_id=post_id))

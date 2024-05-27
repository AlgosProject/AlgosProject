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

        return render_template("media_popup.jinja2", post=post, comments=comments, user=user)

    if request.method == "POST":
        user = userDao.User(**session.get("user"))
        post_id = request.form.get("post_id")
        action = request.form.get("action")
        if action in ["like_post", "dislike_post"]:
            post = postDao.find_one(request.form.get("post_id"))

            if post and post.user.id != user.id:
                if action == "like_post":
                    new_user = post.like_post(user)
                    session["user"] = dict(new_user)

                if action == "dislike_post":
                    new_user = post.dislike_post(user)
                    session["user"] = dict(new_user)

            return redirect(url_for("media_popup.popup", post_id=post_id))

        if request.form["action"] == "post_comment":
            post_id = ObjectId(request.form["post_id"])

            commentDao.insert_one({"post_id": post_id, "text": request.form["comment_text"], "user_id": user.id})

            return redirect(url_for("media_popup.popup", post_id=post_id))

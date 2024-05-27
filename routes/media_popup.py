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
        # TODO: Connect and user tags
        user = userDao.User(**session.get("user"))
        post_id = request.form.get("post_id")
        action = request.form.get("action")
        post = postDao.find_one(post_id)
        likes = post.likes
        dislikes = post.dislikes

        if action == "like_post" and post.user.id != user.id:
            if user.id not in likes:
                likes.append(user.id)
                if user.id in dislikes:
                    dislikes.remove(user.id)
                postDao.update_one(post_id, post)
            elif user.id in likes:
                likes.remove(user.id)
                postDao.update_one(post_id, post)
            return redirect(url_for("media_popup.popup", post_id=post_id))

        elif action == "dislike_post" and post.user.id != user.id:
            if user.id not in dislikes:
                dislikes.append(user.id)
                if user.id in likes:
                    likes.remove(user.id)
                postDao.update_one(post_id, post)
            elif user.id in dislikes:
                dislikes.remove(user.id)
                postDao.update_one(post_id, post)
            return redirect(url_for("media_popup.popup", post_id=post_id))

        if request.form["action"] == "post_comment":
            post_id = ObjectId(request.form["post_id"])

            commentDao.insert_one({"post_id": post_id, "text": request.form["comment_text"], "user_id": user.id})

            return redirect(url_for("media_popup.popup", post_id=post_id))

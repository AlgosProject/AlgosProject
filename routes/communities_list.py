from flask import Blueprint, render_template, request, session, url_for, redirect

import model.postDao
from model import userDao, postDao

communitiesList_blueprint = Blueprint("communities_list", __name__, template_folder="templates")


@communitiesList_blueprint.route("/communities_list", methods=["GET", "POST"])
def communities_list():  # put application's code here
    user = userDao.User(**session.get("user"))
    tag_id = request.args.get("id")

    if request.method == "GET":
        tags = user.get_user_tags_ordered_by_affinity()
        tags = [t for t in tags if t["affinity"] > 0]

        if tag_id:
            posts = model.postDao.find_posts_by_tag(tag_id)
            return render_template("communities_list.jinja2", side_items=tags, posts=posts, user=user)
        else:
            return render_template("communities_list.jinja2", side_items=tags, user=user)

    if request.method == "POST":
        user = userDao.User(**session.get("user"))
        post_id = request.form.get("post_id")
        action = request.form.get("action")
        id_parameter = request.form.get("id")
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
            return redirect(url_for("communities_list.communities_list", id=id_parameter))

        elif action == "dislike_post" and post.user.id != user.id:
            if user.id not in dislikes:
                dislikes.append(user.id)
                if user.id in likes:
                    likes.remove(user.id)
                postDao.update_one(post_id, post)
            elif user.id in dislikes:
                dislikes.remove(user.id)
                postDao.update_one(post_id, post)
            return redirect(url_for("communities_list.communities_list", id=id_parameter))

        if action == "leave_community":
            user.leave_tag(request.form["to_leave_community"])
            session["user"] = dict(user)

            return redirect(url_for("communities_list.communities_list"))

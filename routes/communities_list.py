from flask import Blueprint, render_template, request, session, url_for, redirect

import model.postDao
from model import userDao, postDao
from utils import check_logged_in

communitiesList_blueprint = Blueprint("communities_list", __name__, template_folder="templates")


@communitiesList_blueprint.route("/communities_list", methods=["GET", "POST"])
def communities_list():  # put application's code here
    status = check_logged_in.check_session()
    if status:
        return status
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
        id_parameter = request.form.get("id")

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

            return redirect(url_for("communities_list.communities_list", id=id_parameter))

        if action == "leave_community":
            user.leave_tag(request.form["to_leave_community"])
            session["user"] = dict(user)

            return redirect(url_for("communities_list.communities_list"))

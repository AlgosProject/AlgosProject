from flask import Blueprint, render_template, request, session, url_for, redirect

import model.postDao
from model import userDao

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
            return render_template("communities_list.jinja2", side_items=tags, posts=posts)
        else:
            return render_template("communities_list.jinja2", side_items=tags)

    if request.method == "POST":
        if request.form["action"] == "leave_community":
            user.leave_tag(request.form["to_leave_community"])
            session["user"] = dict(user)

        return redirect(url_for("communities_list.communities_list"))

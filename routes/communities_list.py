from flask import Blueprint, render_template, request, session

from model import userDao

communitiesList_blueprint = Blueprint("communities_list", __name__, template_folder="templates")


@communitiesList_blueprint.route("/communities_list")
def communities_list():  # put application's code here
    user = userDao.User(**session.get("user"))

    if request.method == "GET":
        tags = user.get_user_tags_ordered_by_affinity()
        tags = [t for t in tags if t["affinity"] > 0]

        return render_template("communities_list.jinja2", side_items=tags)
    if request.method == "POST":
        return render_template("communities_list.jinja2")

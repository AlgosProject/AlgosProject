from flask import Blueprint, render_template, session

from model import userDao, postDao

home_blueprint = Blueprint("home_page", __name__, template_folder="templates")


@home_blueprint.route("/home_page")
def home():  # put application's code here

    user = userDao.User(**session.get("user"))

    user.get_friends_dict()
    print(user.get_friends_dict())

    user.bfs_get_visible_user_ids()

    return render_template("home_page.jinja2")

from flask import Blueprint, render_template, session

from model import userDao

friendsList_blueprint = Blueprint("friends_list", __name__, template_folder="templates")


@friendsList_blueprint.route("/friends_list")
def friends_list():  # put application's code here
    user = session.get("user")
    user = userDao.User(**user)
    friends_dict = user.get_friends_dict()

    friends_ls = [userDao.find_one(id) for id in friends_dict.keys()]
    common_friends = dict()

    for fr in friends_ls:
        common_friends[fr.id] = len(set(fr.get_friends_dict().keys()).intersection(set(friends_dict.keys())))

    return render_template("friends_list.jinja2", friends_ls=friends_ls, common_friends=common_friends)

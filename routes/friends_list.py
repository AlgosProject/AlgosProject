from flask import Blueprint, render_template

friendsList_blueprint = Blueprint("friends_list", __name__, template_folder="templates")


@friendsList_blueprint.route("/friends_list")
def friends_list():  # put application's code here
    return render_template("friends_list.jinja2")

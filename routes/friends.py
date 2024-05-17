from flask import Blueprint, render_template

friends_blueprint = Blueprint("friends", __name__, template_folder="templates")


@friends_blueprint.route("/friends")
def friends():  # put application's code here
    return render_template("friends.jinja2")

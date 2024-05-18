from flask import Blueprint, render_template

friendsDiscover_blueprint = Blueprint("friends_discover", __name__, template_folder="templates")


@friendsDiscover_blueprint.route("/friends_discover")
def friends_discover():  # put application's code here
    return render_template("friends_discover.jinja2")

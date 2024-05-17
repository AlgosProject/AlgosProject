from flask import Blueprint, render_template

communities_blueprint = Blueprint("communities", __name__, template_folder="templates")


@communities_blueprint.route("/communities")
def comm():  # put application's code here
    return render_template("communities.jinja2")

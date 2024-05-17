from flask import Blueprint, render_template

communitiesList_blueprint = Blueprint("communities_list", __name__, template_folder="templates")


@communitiesList_blueprint.route("/communities_list")
def communities_list():  # put application's code here
    return render_template("communities_list.jinja2")

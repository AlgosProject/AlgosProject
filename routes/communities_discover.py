from flask import Blueprint, render_template

communitiesDiscover_blueprint = Blueprint("communities_discover", __name__, template_folder="templates")


@communitiesDiscover_blueprint.route("/communities_discover")
def communities_discover():  # put application's code here
    return render_template("communities_discover.jinja2")

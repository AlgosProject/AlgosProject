from flask import Blueprint, render_template

home_blueprint = Blueprint("home_page", __name__, template_folder="templates")


@home_blueprint.route("/home_page")
def home():  # put application's code here
    return render_template("home_page.jinja2")

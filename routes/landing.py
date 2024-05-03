from flask import Blueprint, render_template

landing_blueprint = Blueprint("landing", __name__, template_folder="templates")


@landing_blueprint.route("/")
def hello_world():  # put application"s code here
    data = ["Hello", "World!"]
    return render_template("Hello_world.jinja2", data=data)

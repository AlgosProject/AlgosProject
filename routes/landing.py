from flask import Blueprint, render_template

landing_blueprint = Blueprint("landing", __name__, template_folder="templates")


@landing_blueprint.route("/old_landing")
def hello_world():  # put applications code here
    data = ["Hello", "World!"]
    return render_template("Hello_world.jinja2", data=data)

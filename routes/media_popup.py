from flask import Blueprint, render_template

popup_blueprint = Blueprint("media_popup", __name__, template_folder="templates")


@popup_blueprint.route("/media")
def popup():  # put application's code here
    return render_template("media_popup.jinja2")

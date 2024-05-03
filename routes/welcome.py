from flask import Blueprint, render_template

welcome_blueprint = Blueprint("welcome", __name__, template_folder="templates")


@welcome_blueprint.route("/welcome/<user>/<psw>")
def welcome(user, psw):
    return render_template('welcome.jinja2', data=[user, psw])

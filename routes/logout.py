from flask import Blueprint, request, render_template, redirect, url_for, session
from model import userDao

logout_blueprint = Blueprint('logout', __name__,
                                 template_folder='templates')


@logout_blueprint.route("/logout", methods=["GET"])
def login_form():
    session.clear()
    return render_template("login_form.jinja2")
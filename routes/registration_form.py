from flask import Blueprint, request, render_template, redirect, url_for, current_app, session
from model import userDao

registration_form_blueprint = Blueprint('registration_form', __name__, template_folder='templates')


@registration_form_blueprint.route("/registration_form")
def registration_form():
    return render_template("registration_form.jinja2")

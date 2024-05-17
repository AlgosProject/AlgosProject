from flask import Blueprint, request, render_template, redirect, url_for, current_app, session
from model import userDao

login_form_blueprint = Blueprint('login_form', __name__,
                                 template_folder='templates')


@login_form_blueprint.route("/login_form", methods=["GET", "POST"])
def login_form():
    if request.method == "POST":
        user = request.form["user"]
        psw = request.form["pass"]

        log_user = userDao.login(user, psw)
        if log_user:
            session['user'] = dict(log_user)
            return redirect(url_for("welcome.welcome", user=user, psw=psw))
        else:
            pass
            # TODO: Failed authentication

    elif request.method == "GET":
        return render_template("login_form.jinja2")

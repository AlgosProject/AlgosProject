from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from model import userDao

login_form_blueprint = Blueprint('login_form', __name__,
                                 template_folder='templates')


@login_form_blueprint.route("/", methods=["GET", "POST"])
def login_form():
    if request.method == "POST":
        session.clear()
        user = request.form["user"]
        psw = request.form["password"]

        log_user = userDao.login(user, psw)
        if log_user:
            flash("You are now logged in!", "success")
            session['user'] = dict(log_user)
            session['logged_in'] = True
            return redirect(url_for("home_page.home"))
        else:
            return render_template("login_form.jinja2", error="Invalid Credentials")

    elif request.method == "GET":
        return render_template("login_form.jinja2")

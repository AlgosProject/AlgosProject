from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from model import userDao
from utils import check_logged_in

profileSettings_blueprint = Blueprint("profile_settings", __name__, template_folder="templates")


@profileSettings_blueprint.route("/profile_settings", methods=["GET", "POST"])
def profile_settings():  # put application's code here
    status = check_logged_in.check_session()
    if status:
        return status
    if request.method == "GET":
        return render_template("profile_settings.jinja2")

    if request.method == "POST":
        user = userDao.User(**session.get("user"))
        calltype = request.form.get("update")
        if calltype == "username":
            username = request.form.get("username")
            session['user'] = dict(user.set_username(username))
        elif calltype == "password":
            from flask import current_app
            from flask_bcrypt import Bcrypt

            bcrypt: Bcrypt = current_app.bcrypt
            password = request.form.get("password")
            password = bcrypt.generate_password_hash(password)
            session['user'] = dict(user.set_password(password))
        elif calltype == "name":
            name = request.form.get("name")
            session['user'] = dict(user.set_name(name))
        elif calltype == "picture":
            from utils import cloudinary_upload
            picture = request.files["profile_picture"]
            picture_url = cloudinary_upload.upload(picture)
            session["user"] = dict(user.set_photo_url(picture_url))
        elif calltype == "privacy_control":
            privacy_control = int(request.form.get("privacy_control"))
            session['user'] = dict(user.set_privacy_control(privacy_control))
        flash("Updated " + calltype + " successfully")
        return render_template("profile_settings.jinja2")

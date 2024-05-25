from flask import Blueprint, request, render_template, redirect, url_for, current_app, session
from model import userDao
from utils import cloudinary_upload
from flask_bcrypt import Bcrypt

registration_form_blueprint = Blueprint('registration_form', __name__, template_folder='templates')


@registration_form_blueprint.route("/registration_form", methods=["GET", "POST"])
def registration_form():
    if request.method == "GET":
        return render_template("registration_form.jinja2")

    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        privacy_level = request.form['privacy_level']
        print(username, password, name, privacy_level)
        bcrypt: Bcrypt = current_app.bcrypt
        image = request.files['profile_picture']
        photo_url = cloudinary_upload.upload(image)
        privacy_level = int(privacy_level)
        ps_hash = bcrypt.generate_password_hash(password)
        userDao.insert_one({
            "friends": [],
            "name": name,
            "username": username,
            "password": ps_hash,
            "photo_url": photo_url,
            "privacy_control": privacy_level,
            "seen": [],
            "tags": []
        })
        session["success"] = "Account Created!"
        return redirect(url_for("login_form.login_form"))



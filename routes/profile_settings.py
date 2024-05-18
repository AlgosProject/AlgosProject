from flask import Blueprint, render_template

profileSettings_blueprint = Blueprint("profile_settings", __name__, template_folder="templates")


@profileSettings_blueprint.route("/profile_settings")
def profile_settings():  # put application's code here
    return render_template("profile_settings.jinja2")

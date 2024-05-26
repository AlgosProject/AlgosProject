from flask import Blueprint, render_template

notification_blueprint = Blueprint("notification", __name__, template_folder="templates")


@notification_blueprint.route("/notification")
def notification():
    return render_template('notification.jinja2')

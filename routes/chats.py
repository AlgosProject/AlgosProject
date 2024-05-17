from flask import Blueprint, render_template

chats_blueprint = Blueprint("chats", __name__, template_folder="templates")


@chats_blueprint.route("/chats")
def chat():  # put application's code here
    return render_template("chats.jinja2")

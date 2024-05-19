from flask import Blueprint, render_template

profilePosts_blueprint = Blueprint("profile_posts", __name__, template_folder="templates")


@profilePosts_blueprint.route("/profile_posts")
def friends_list():  # put application's code here
    return render_template("profile_posts.jinja2")

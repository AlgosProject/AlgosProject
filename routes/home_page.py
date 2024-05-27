from flask import Blueprint, render_template, session, request, redirect, url_for

from model import userDao, postDao
from utils import check_logged_in

home_blueprint = Blueprint("home_page", __name__, template_folder="templates")


@home_blueprint.route("/home_page", methods=["GET", "POST"])
def home():
    status = check_logged_in.check_session()
    if status:
        return status
      
    # Get the user from session
    user = userDao.User(**session.get("user"))
      
    if request.method == "GET":

        # Get the users he can see
        visible_user = user.bfs_get_visible_user_ids()

        # Get the posts he can see and prepares them for the view
        posts = []
        for u_id in visible_user:
            u_posts = postDao.find_posts_by_user(u_id)
            for p in u_posts:
                posts.append(p)

        return render_template("home_page.jinja2", posts=posts, user=user)

    if request.method == "POST":
        action = request.form.get("action")
        if action in ["like_post", "dislike_post"]:
            post = postDao.find_one(request.form.get("post_id"))

            if post and post.user.id != user.id:
                if action == "like_post":
                    new_user = post.like_post(user)
                    session["user"] = dict(new_user)

                if action == "dislike_post":
                    new_user = post.dislike_post(user)
                    session["user"] = dict(new_user)

        return redirect(url_for("home_page.home"))

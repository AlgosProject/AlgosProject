from flask import Blueprint, render_template, session

from model import userDao, postDao

home_blueprint = Blueprint("home_page", __name__, template_folder="templates")


@home_blueprint.route("/home_page")
def home():
    # Get the user from session and the users he can see
    user = userDao.User(**session.get("user"))
    visible_user = user.bfs_get_visible_user_ids()

    # Get the posts he can see and prepares them for the view
    posts = []
    for u_id in visible_user:
        u_posts = postDao.find_posts_by_user(u_id)
        for p in u_posts:
            p.user = userDao.find_one(p.user_id)
            p.likes_amount = len(p.likes)
            p.id = p.get_id()
            posts.append(p)

    return render_template("home_page.jinja2", posts=posts)

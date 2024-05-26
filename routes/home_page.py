from flask import Blueprint, render_template, session, request

from model import userDao, postDao

home_blueprint = Blueprint("home_page", __name__, template_folder="templates")


@home_blueprint.route("/home_page", methods=["GET", "POST"])
def home():
    # Get the user from session
    user = userDao.User(**session.get("user"))

    if request.method == "POST":
        post_id = request.form.get("post_id")
        action = request.form.get("action")
        post = postDao.find_one(post_id)
        likes = post.likes
        dislikes = post.dislikes

        if post and post.user.id != user.id:
            if action == "like_post":
                if user.id not in likes:
                    likes.append(user.id)
                    if user.id in dislikes:
                        dislikes.remove(user.id)
                    postDao.update_one(post_id, post)
                elif user.id in likes:
                    likes.remove(user.id)
                    postDao.update_one(post_id, post)
            elif action == "dislike_post":
                if user.id not in dislikes:
                    dislikes.append(user.id)
                    if user.id in likes:
                        likes.remove(user.id)
                    postDao.update_one(post_id, post)
                elif user.id in dislikes:
                    dislikes.remove(user.id)
                    postDao.update_one(post_id, post)

    # Get the users he can see
    visible_user = user.bfs_get_visible_user_ids()

    # Get the posts he can see and prepares them for the view
    posts = []
    for u_id in visible_user:
        u_posts = postDao.find_posts_by_user(u_id)
        for p in u_posts:
            posts.append(p)

    return render_template("home_page.jinja2", posts=posts, user=user)

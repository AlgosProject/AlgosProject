from bson import ObjectId
from flask import Blueprint, render_template, session, request, redirect, url_for

from model import userDao, postDao

profilePosts_blueprint = Blueprint("profile_posts", __name__, template_folder="templates")


@profilePosts_blueprint.route("/profile_posts/<profile_id>", methods=['GET', 'POST'])
@profilePosts_blueprint.route("/profile_posts", defaults={'profile_id': None}, methods=['GET', 'POST'])
def profile_posts(profile_id=None):
    if request.method == "GET":
        curr_user = True
        user = session.get('user')
        current_user_id = user.get('_id')
        profile = userDao.find_one(current_user_id)

        user = userDao.User(**user)
        friends_dict = user.get_friends_dict()

        friends_ls = [userDao.find_one(id) for id in friends_dict.keys()]
        common_friends = dict()

        for fr in friends_ls:
            common_friends[fr.id] = len(set(fr.get_friends_dict().keys()).intersection(set(friends_dict.keys())))

        if profile_id:
            profile2 = userDao.find_one(profile_id)
            curr_user = True if profile2 == profile else False
            profile = profile2

        u_posts = postDao.find_posts_by_user(profile.id)
        posts = []

        for p in u_posts:
            posts.append(p)

        return render_template("profile_posts.jinja2", profile=profile, posts=posts,
                               curr_user=curr_user, common_friends=common_friends, user=user)

    if request.method == "POST":
        user = userDao.User(**session.get("user"))
        profile_id = request.form.get("profile_id")

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

        if profile_id:
            return redirect(url_for("profile_posts.profile_posts", profile_id=profile_id, _external=True))
        else:
            return redirect(url_for("profile_posts.profile_posts"))

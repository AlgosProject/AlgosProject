from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from model import userDao, postDao
from model import tagDao
from utils import check_logged_in

search_page_blueprint = Blueprint('search_page', __name__,
                                 template_folder='templates')


@search_page_blueprint.route("/search_page", methods=["GET", "POST"])
def login_form():
    status = check_logged_in.check_session()
    if status:
        return status
    if request.method == "POST":
        user = session.get("user")
        user = userDao.User(**user)
        friends_dict = user.get_friends_dict()
        query = request.form["query"]
        query = query.lower()
        tags = tagDao.get_all_like(query)
        friends_ls = userDao.get_user_like_name(query)
        common_friends = dict()
        for fr in friends_ls:
            common_friends[fr.id] = len(set(fr.get_friends_dict().keys()).intersection(set(friends_dict.keys())))
        posts = postDao.get_all_like(query)
        filterposts = []
        visitable_ids = user.bfs_get_visible_user_ids()
        for post in posts:
            if post.user_id in visitable_ids:
                filterposts.append(post)
        return render_template("search_page.jinja2", query=query, tags=tags, friends_ls=friends_ls,
                               common_friends=common_friends, posts=filterposts)

    elif request.method == "GET":
        return render_template("search_page.jinja2")

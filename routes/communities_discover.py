from flask import Blueprint, render_template, session, request, redirect, url_for

from model import userDao
from utils import check_logged_in

communitiesDiscover_blueprint = Blueprint("communities_discover", __name__, template_folder="templates")


@communitiesDiscover_blueprint.route("/communities_discover", methods=["GET", "POST"])
def communities_discover():
    status = check_logged_in.check_session()
    if status:
        return status
    user = userDao.User(**session["user"])

    if request.method == "GET":
        visible_user_ids = user.bfs_get_visible_user_ids()
        joined_tags = [t["tag"] for t in user.get_user_tags_ordered_by_affinity() if t["affinity"] > 0]

        tags = []

        for u_id in visible_user_ids:
            vis_user = userDao.find_user_by_id(u_id)
            other_tags = [t["tag"] for t in vis_user.get_user_tags_ordered_by_affinity() if t["affinity"] > 0]
            for t in other_tags:
                if t not in joined_tags and t not in tags:
                    tags.append(t)


        return render_template("communities_discover.jinja2", tags=tags)

    if request.method == "POST":
        if request.form["action"] == "join_community":
            user.joint_tag(request.form["to_join_community"])
        return redirect(url_for("communities_discover.communities_discover"))
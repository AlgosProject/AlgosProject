from flask import Blueprint, render_template, session

from model import notificationDao, userDao

friendsDiscover_blueprint = Blueprint("friends_discover", __name__, template_folder="templates")


@friendsDiscover_blueprint.route("/friends_discover")
def friends_discover():
    user = userDao.User(**session["user"])
    friend_requests = user.fr_notifications
    friend_requests = [f.author for f in friend_requests]
    common_friends = dict()
    notifs = dict()

    for u in friend_requests:
        common_friends[u.id] = len(user.get_common_friends(u.id))

    for n in user.fr_notifications:
        notifs[n.author_id] = n.id

    visible_user = user.bfs_get_visible_user_ids()
    visible_user = [userDao.find_one(u) for u in visible_user]
    visible_user.sort(key=lambda other_id: user.compare_affinity(other_id))

    return render_template("friends_discover.jinja2",
                           pending_fr=friend_requests,
                           common_friends=common_friends,
                           notifs=notifs,
                           empty_fr=not bool(len(friend_requests))
                           )

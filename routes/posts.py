from bson import ObjectId
from flask import Blueprint, render_template, session, request, redirect, url_for, flash

from model import userDao, postDao, tagDao

from utils import cloudinary_upload

new_post_blueprint = Blueprint("new_post", __name__, template_folder="templates")


@new_post_blueprint.route("/new-post", methods=["GET", "POST"])
def new_post():  # put application's code here
    user = userDao.User(**session.get("user"))

    if request.method == "GET":
        return render_template(
            "new-post.jinja2",
            current_uid=user.id,
        )

    if request.method == "POST":
        image = request.files["post-img"]
        post_img_url = cloudinary_upload.upload(image)
        caption = request.form.get("post_caption")
        tags = request.form.get("taglist")
        taglist = tags.split(",")
        tagObjList = []
        for tag in taglist:
            tag = tag.strip()
            tag = tag.lower()
            if tag == "" or tag == " ":
                continue
            tag = tag.replace(" ", "_")
            tagobj = tagDao.find_by_name(tag)
            if tagobj is None:
                tagobj = tagDao.insert_one({"name": tag, "post_ids": []})
                tagobj = tagDao.find_one(tagobj)
            else:
                tagobj = tagobj
            tagObjList.append(tagobj)
        tagidlist = [x.id for x in tagObjList]
        post_id = postDao.insert_one({"likes": [], "photo_url": post_img_url,
                                      "text": caption, "user_id": user.id,
                                      "comments": [], "tags": tagidlist})
        for tag in tagObjList:
            tag.add_post(post_id)
        flash("New post has been successfully uploaded!", "success")
        return redirect(url_for("home_page.home"))

from bson import ObjectId
from flask import Blueprint, render_template, session, request, redirect, url_for, flash

from model import userDao, postDao, tagDao

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
        from dotenv import load_dotenv
        load_dotenv()

        import cloudinary
        from cloudinary import CloudinaryImage
        import cloudinary.uploader
        import cloudinary.api

        file_to_upload = request.files['post-img']
        post_img_url = ""
        if file_to_upload:
            upload_result = cloudinary.uploader.upload(file_to_upload)
            post_img_url = upload_result["url"]
        caption = request.form.get("post_caption")
        tags = request.form.get("taglist")
        taglist = tags.split(",")
        tagObjList = []
        for tag in taglist:
            tag = tag.strip()
            tag = tag.lower()
            tag = tag.replace(" ", "_")
            tagobj = tagDao.find_by_name(tag)
            if tagobj is None:
                tagobj = tagDao.insert_one({"name": tag, "post_ids": []})
            else:
                tagobj = tagobj.id
            tagObjList.append(tagobj)
        postDao.insert_one({"likes":[], "photo_url": post_img_url, "text": caption, "user_id": user.id, "comments": [], "tags": tagObjList})
        flash("New post has been successfully uploaded!", "success")
        return redirect(url_for("home_page.home"))

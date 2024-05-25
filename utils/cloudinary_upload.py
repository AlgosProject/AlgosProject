from dotenv import load_dotenv

import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api

load_dotenv()


def upload(file_to_upload):
    post_img_url = ""
    if file_to_upload:
        upload_result = cloudinary.uploader.upload(file_to_upload)
        post_img_url = upload_result["url"]
    return post_img_url

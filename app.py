import os
import certifi

from flask import Flask
from flask_session import Session
from routes.login_form import login_form_blueprint
from routes.landing import landing_blueprint
from routes.welcome import welcome_blueprint
from cachelib import FileSystemCache
from routes.home_page import home_blueprint
from routes.media_popup import popup_blueprint
from routes.friends_list import friendsList_blueprint
from routes.communities_list import communitiesList_blueprint
from routes.chats import chats_blueprint
from routes.friends_discover import friendsDiscover_blueprint
from routes.communities_discover import communitiesDiscover_blueprint
from routes.profile_settings import profileSettings_blueprint
from routes.profile_posts import profilePosts_blueprint
from routes.registration_form import registration_form_blueprint
from routes.posts import new_post_blueprint
from routes.logout import logout_blueprint
from routes.notification import notification_blueprint
from routes.search_page import search_page_blueprint
from routes.add_friend import add_friend_blueprint

from utils.mongo_store_broker import mongo
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DB_PASSWORD = "example"
DB_USER = "mongo"
DB_URL = "localhost"
DB_PORT = "27017"

mongo_url = os.environ.get("MONGO_URL")
if not mongo_url:
    mongo_url = "mongodb://localhost:27017"

mongo.init_app(app, uri=mongo_url, tlsCAFile=certifi.where())

app.bcrypt = Bcrypt(app)

SESSION_TYPE = 'cachelib'
SESSION_SERIALIZATION_FORMAT = 'json'
SESSION_CACHELIB = FileSystemCache(threshold=500, cache_dir="/sessions")

app.config.from_object(__name__)
app.session = Session(app)

app.register_blueprint(login_form_blueprint)
app.register_blueprint(landing_blueprint)
app.register_blueprint(welcome_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(popup_blueprint)
app.register_blueprint(friendsList_blueprint)
app.register_blueprint(communitiesList_blueprint)
app.register_blueprint(chats_blueprint)
app.register_blueprint(friendsDiscover_blueprint)
app.register_blueprint(communitiesDiscover_blueprint)
app.register_blueprint(profileSettings_blueprint)
app.register_blueprint(profilePosts_blueprint)
app.register_blueprint(registration_form_blueprint)
app.register_blueprint(new_post_blueprint)
app.register_blueprint(logout_blueprint)
app.register_blueprint(search_page_blueprint)
app.register_blueprint(notification_blueprint)
app.register_blueprint(add_friend_blueprint)

if __name__ == "__main__":
    app.run()

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

from utils.mongo_store_broker import mongo
from flask_bcrypt import Bcrypt

app = Flask(__name__)

DB_PASSWORD = "example"
DB_USER = "mongo"
DB_URL = "localhost"
DB_PORT = "27017"

mongo.init_app(app, uri=f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_URL}:{DB_PORT}/algos_project?authSource=admin")

app.bcrypt = Bcrypt(app)

SESSION_TYPE = 'cachelib'
SESSION_SERIALIZATION_FORMAT = 'json'
"""SESSION_CACHELIB = FileSystemCache(threshold=500, cache_dir="/sessions") """

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

if __name__ == "__main__":
    app.run()

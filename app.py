from flask import Flask
from routes.login_form import login_form_blueprint
from routes.landing import landing_blueprint
from routes.welcome import welcome_blueprint
from utils.mongo_store_broker import mongo


DB_PASSWORD = "example"
DB_USER = "mongo"
DB_URL = "localhost"
DB_PORT = "27017"

app = Flask(__name__)

mongo.init_app(app, uri=f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_URL}:{DB_PORT}/algos_project?authSource=admin")

app.register_blueprint(login_form_blueprint)
app.register_blueprint(landing_blueprint)
app.register_blueprint(welcome_blueprint)


if __name__ == "__main__":
    app.run()

from flask import Flask, render_template
from routes.login_form import login_form_blueprint
from routes.landing import landing_blueprint
from routes.welcome import welcome_blueprint
import pymongo


DB_PASSWORD = "example"
DB_USER = "monogo"
DB_URL = "localhost"
DB_PORT = "27017"

db = pymongo.MongoClient(f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_URL}:{DB_PORT}/algos_project")

app = Flask(__name__)

app.register_blueprint(login_form_blueprint)
app.register_blueprint(landing_blueprint)
app.register_blueprint(welcome_blueprint)



if __name__ == "__main__":
    app.run()

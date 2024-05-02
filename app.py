from flask import Flask, render_template, request, redirect, url_for
import pymongo

DB_PASSWORD = "example"
DB_USER = "monogo"
DB_URL = "localhost"
DB_PORT = "27017"

db = pymongo.MongoClient(f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_URL}:{DB_PORT}/algos_project")

app = Flask(__name__)


@app.route("/")
def hello_world():  # put application"s code here
    data = ["Hello", "World!"]
    return render_template("Hello_world.jinja2", data=data)


@app.route("/login_form", methods=["GET", "POST"])
def login_form():
    if request.method == "POST":
        print(request.form)
        user = request.form["user"]
        psw = request.form["pass"]
        return redirect(url_for("welcome", user=user, psw=psw))
    elif request.method == "GET":
        return render_template("login_form.jinja2")


@app.route("/welcome/<user>/<psw>")
def welcome(user, psw):
    return render_template('welcome.jinja2', data=[user, psw])


if __name__ == "__main__":
    app.run()

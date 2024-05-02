from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    data = ["Hello", "8"]
    return render_template("Hello_world.html", data=data)


if __name__ == '__main__':
    app.run()

import requests
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/login")
def hello_world():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/search")
def search():
    return render_template("search.html")


if __name__ == "__main__":
    app.run(debug=True)
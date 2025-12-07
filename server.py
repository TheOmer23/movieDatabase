# server.py
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, flash
from main import signup as signup_user
from main import movie_check          # <-- add this
from passwords import flask_key

app = Flask(__name__)
app.secret_key = flask_key

@app.route("/login")
def login_route():
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup_route():
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            signup_user(email, password)
            flash("Account created successfully!", "success")
            return redirect(url_for("login_route"))
        except Exception as e:
            flash(f"An error occurred during signup: {e}", "danger")
    return render_template("signup.html")

@app.route("/", methods=["GET", "POST"])
def search_route():
    return render_template("search.html")

@app.route("/search", methods=["GET"])
def search():
    movie_name = request.args.get("movie_name")
    posters = []
    movie_data = None

    if movie_name:
        # get full JSON
        movie_data = movie_check(movie_name)
        # still keep poster list for display
        if movie_data and movie_data.get("Response") == "True":
            posters = [m["Poster"] for m in movie_data["Search"]]

    return render_template(
        "search.html",
        posters=posters,
        movie_name=movie_name,
        movie_data=movie_data
    )

@app.route("/movie_page", methods=["GET"])
def movie_page():
    # All data is coming from the query string
    movie = request.args.to_dict()
    return render_template("movie_page.html", movie=movie)

if __name__ == "__main__":
    app.run(debug=True)

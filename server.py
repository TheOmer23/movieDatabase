# from crypt import methods
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, flash
from main import signup as signup_user
from main import get_movie_poster
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
            # Signup succeeded, redirect to login page
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
    posters = None
    if movie_name:
        posters = get_movie_poster(movie_name)
    return render_template("search.html", posters=posters, movie_name=movie_name)

@app.route("/movie_page", methods=["GET"])
def movie_page():
    
    return render_template("movie_page.html")
    
    


if __name__ == "__main__":
    app.run(debug=True)
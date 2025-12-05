from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, flash
from main import signup as signup_user

app = Flask(__name__)
app.secret_key = "your_secret_key"

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

@app.route("/search")
def search_route():
    return render_template("search.html")


if __name__ == "__main__":
    app.run(debug=True)
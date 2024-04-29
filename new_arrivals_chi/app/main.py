"""
Project: new_arrivals_chi
File name: main.py
Associated Files:
    Templates: base.html, home.html, legal.html, profile.html, signup.html,
    login.html

Runs primary flask application for Chicago's new arrivals portal.

Methods:
    * home — Route to homepage of application.
    * profile - Route to user's profil.
    * legal - Route to legal portion of application.

Last updated:
@Author: Madeleine Roberts @MadeleineKRoberts
@Date: 04/25/2024

Creation:
@Author: Summer Long @Sumslong
@Date: 04/19/2024
"""

from flask import Flask, Blueprint, render_template, request

main = Blueprint("main", __name__, static_folder="/static")


@main.route("/")
def home():
    language = request.args.get("lang", "en")
    return render_template("home.html", language=language)


@main.route("/profile")
def profile():
    """
    Establishes route for the user's profile page. This route is accessible
    within the 'profile' button in the navigation bar.

    Returns:
        Renders profile page for user with in their selected language.
    """

    language = request.args.get("lang", "en")
    return render_template("profile.html", language=language)


@main.route("/legal")
def legal():
    language = request.args.get("lang", "en")
    return render_template("legal.html", language=language)


# will change to auth.route when the database is usable
@main.route("/login")
def login():
    """
    Establishes route for the login page. This route is accessible
    within the 'login' button in the navigation bar.

    Returns:
        Renders login page for user with their selected language.
    """

    language = request.args.get("lang", "en")
    return render_template("login.html", language=language)


# @auth.route('/signup')
@main.route("/signup")
def signup():
    """
    Establishes route for the user sign up page. This route is accessible
    within the 'sign up' button in the navigation bar.

    Returns:
        Renders sign up page in their selected language.
    """

    language = request.args.get("lang", "en")
    return render_template("signup.html", language=language)


app = Flask(__name__)

app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)

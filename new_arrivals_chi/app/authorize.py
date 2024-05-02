# will change to auth.route when the database is usable
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from flask_login import login_user, login_required, logout_user, current_user
import re

authorize = Blueprint("authorize", __name__, static_folder="/static")

@authorize.route("/login")
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
@authorize.route("/signup")
def signup():
    """
    Establishes route for the user sign up page. This route is accessible
    within the 'sign up' button in the navigation bar.

    Returns:
        Renders sign up page in their selected language.
    """

    language = request.args.get("lang", "en")
    return render_template("signup.html", language=language)
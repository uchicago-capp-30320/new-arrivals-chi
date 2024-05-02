"""
Project: new_arrivals_chi
File name: authorize.py
Associated Files:
    Templates: profile.html, signup.html, login.html

Defines routes for user creation and authentication for new arrivals portal.

Methods:
    * login - Route to the login page.
    * signup - Route to the user sign up page.
    * signup_post - Handles the POST request for user sign up.

Last updated:
@Author: Madeleine Roberts @MadeleineKRoberts
@Date: 05/01/2024

Creation:
@Author: Madeleine Roberts @MadeleineKRoberts
@Date: 05/01/2024
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
from database import db, User
from utils import validate_email_syntax, validate_password

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


@authorize.route("/signup", methods=["POST"])
def signup_post():
    """
    Handles the POST request for user sign up. Validates the input data,
    adds the user to the database if valid, and redirects accordingly.

    Returns:
        Redirects to the home page upon successful sign up.
        Redirects back to the sign up page if there are validation errors
        or if the email address already exists in the database.
    """

    email = request.form.get("email")
    password = request.form.get("password")

    # ensure that input meets requirments
    email_synax = validate_email_syntax(email)

    if not email_synax:
        flash("Please enter a valid email address")
        return redirect(url_for("authorize.signup"))

    # password constraints: 8+ characters, 1+ number, 1+ special characters
    # cannot be empty, cannot contain certain special chars, no spaces
    password_strength = validate_password(password)

    if not password_strength:
        flash("Please enter a valid password")
        return redirect(url_for("authorize.signup"))

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()

    if user:
        # if a user is found, we want to redirect back to signup page
        flash("Email address already exists for user")
        return redirect(url_for("authorize.signup"))

    # create a new user with the form data
    new_user = User(
        email=email,
        password=generate_password_hash(password, method="pbkdf2:sha256"),
    )
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("main.home"))
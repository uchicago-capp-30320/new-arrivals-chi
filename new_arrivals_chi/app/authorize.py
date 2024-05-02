"""
Project: new_arrivals_chi
File name: authorize.py
Associated Files:
    Templates: profile.html, signup.html, login.html

Defines routes for user creation and authentication for new arrivals portal.

Methods:
    * signup - Route to the user sign up page.
    * signup_post - Executes user sign up logic.
    * login - Route to the login page.
    * login_post - Executes user login logic.
    * signout - Routes and executes user sign out logic.

Last updated:
@Author: Madeleine Roberts @MadeleineKRoberts
@Date: 05/02/2024

Creation:
@Author: Madeleine Roberts @MadeleineKRoberts
@Date: 05/01/2024
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User
from utils import validate_email_syntax, validate_password
from flask_login import login_user, login_required, logout_user, current_user

authorize = Blueprint("authorize", __name__, static_folder="/static")


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


@authorize.route("/login", methods=["POST"])
def login_post():
    """
    Processes the login request.

    Returns:
        Redirects to the user's profile page if login is successful,
        otherwise redirects back to the login page with a flash message.
    """

    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists & password is correct
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(
            url_for("authorize.login")
        )  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for("main.profile"))


@authorize.route("/logout")
@login_required
def logout():
    """
    Logs out the current user.

    Returns:
        Redirects to the home page after logout.
        If a user is not currently logged in, redirects to the log in page.
    """

    logout_user()
    return redirect(url_for("main.home"))


@authorize.route("/change_password")
@login_required
def change_password():
    """
    Establishes route for the change password page. This route is accessible
    within the 'change password' button in the profile page (will likely change
    location in the future).

    Returns:
        Renders change password page for user with their selected language.
    """

    language = request.args.get("lang", "en")
    return render_template("change_password.html", language=language)


@authorize.route("/change_password", methods=["POST"])
@login_required
def post_change_password():
    """
    Allows an authorized user to update their current password.

    Returns:
        Redirects to the user's profile page if password change is successful,
        otherwise redirects back to the change password page with a flash
        message.
    """

    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    new_password_confirm = request.form.get("new_password_confirm")

    if not check_password_hash(current_user.password, old_password):
        flash("Wrong existing password. Try again")
    elif (
        old_password == new_password
    ):  # Do not need to check password hash because old password is correct
        flash("New password cannot be the same as your previous password.")
    elif not new_password == new_password_confirm:
        flash("New passwords do not match. Try again")
    elif not validate_password(new_password):
        flash("New password does not meet requirements. Try again")
    else:
        current_user.password = generate_password_hash(
            new_password, method="pbkdf2:sha256"
        )
        db.session.commit()
        flash("Password change successful.")
        return redirect(url_for("main.profile"))

    return redirect(url_for("authorize.change_password"))

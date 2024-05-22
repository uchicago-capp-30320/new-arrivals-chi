"""Project: new_arrivals_chi.

File name: authorize_routes.py
Associated Files:
    Templates: dashboard.html, signup.html, login.html.

Defines routes for user creation and authentication for new arrivals portal.

Methods:
    * signup - Route to the user sign up page.
    * signup_post - Executes user sign up logic.
    * login - Route to the login page.
    * login_post - Executes user login logic.
    * signout - Routes and executes user sign out logic.
    * change_password - Route to the change password page.
    * post_change_password - Executes change password logic.

Last updated:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/09/2024

Creation:
@Author: Madeleine Roberts @MadeleineKRoberts
@Date: 05/01/2024
"""

import bleach
from markupsafe import escape
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    current_app,
)
from new_arrivals_chi.app.database import User
from new_arrivals_chi.app.utils import (
    validate_email_syntax,
    validate_password,
    extract_signup_data,
    extract_new_pw_data,
    verify_password,
)
from new_arrivals_chi.app.constants import (
    KEY_TRANSLATIONS,
    KEY_LANGUAGE,
    DEFAULT_LANGUAGE,
)
from flask_login import login_user, login_required, logout_user, current_user
from new_arrivals_chi.app.data_handler import create_user, change_db_password


authorize = Blueprint("authorize", __name__, static_folder="/static")


@authorize.route("/signup")
def signup():
    """Establishes route for the user sign up page.

    This route is accessible within the 'sign up' button in the navigation bar.


    Returns:
        Renders sign up page in their selected language.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]
    return render_template(
        "signup.html", language=language, translations=translations
    )


@authorize.route("/signup", methods=["POST"])
def signup_post():
    """Handles the POST request for user sign up.

    Validates the input data, adds the user to the database if valid, and
    redirects accordingly.

    Returns:
        Redirects to the home page upon successful sign up.
        Redirects back to the sign-up page if there are validation errors
        or if the email address already exists in the database.
    """
    email, password, password_confirm = extract_signup_data(request.form)

    # ensure that input meets requirments
    if not validate_email_syntax(email):
        flash(escape("Please enter a valid email address"))

    elif User.query.filter_by(email=email).first():
        # email already exists in database
        flash(escape("Email address already exists for user"))

    elif not password == password_confirm:
        flash(escape("Passwords do not match. Try again"))

    elif not validate_password(password):
        flash(escape("Please enter a valid password"))

    else:
        # Meets all sign up requirements
        new_user = create_user(email, password)
        login_user(new_user, remember=False)
        return redirect(url_for("main.dashboard"))

    return redirect(url_for("authorize.signup"))


@authorize.route("/login")
def login():
    """Establishes route for the login page.

    Login route is accessible within the 'login' button in the navigation bar.

    Returns:
        Renders login page for user with their selected language.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]
    return render_template(
        "login.html", language=language, translations=translations
    )


@authorize.route("/login", methods=["POST"])
def login_post():
    """Processes the login request.

    Returns:
        Redirects to the user's dashboard page if login is successful,
        otherwise redirects back to the login page with a flash message.
    """
    email = request.form.get("email").lower()
    password = request.form.get("password")
    remember = request.form.get("remember", False)

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists & password is correct
    if not user or not verify_password(user.password, password):
        flash(escape("Please check your login details and try again."))
        return redirect(
            url_for("authorize.login")
        )  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for("main.dashboard"))


@authorize.route("/logout")
@login_required
def logout():
    """Logs out the current user.

    Returns:
        Redirects to the home page after logout.
        If a user is not currently logged in, redirects to the log in page.
    """
    logout_user()
    return redirect(url_for("main.home"))


@authorize.route("/change_password")
@login_required
def change_password():
    """Establishes route for the change password page.

    This route is accessible within the 'change password' button in dashboard
    page (will likely change location in the future).

    Returns:
        Renders change password page for user with their selected language.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]
    return render_template(
        "change_password.html", language=language, translations=translations
    )


@authorize.route("/change_password", methods=["POST"])
@login_required
def post_change_password():
    """Allows an authorized user to update their current password.

    Returns:
        Redirects to the user's dashboard page if password change is successful,
        otherwise redirects back to the change password page with a flash
        message.
    """
    old_password, new_password, new_password_confirm = extract_new_pw_data(
        request.form
    )

    if not verify_password(current_user.password, old_password):
        flash(escape("Wrong existing password. Try again"))

    elif old_password == new_password:
        # Do not need to check password hash because old password is correct
        flash(
            escape("New password cannot be the same as your previous password.")
        )

    elif not new_password == new_password_confirm:
        flash(escape("New passwords do not match. Try again"))

    elif not validate_password(new_password):
        flash(escape("New password does not meet requirements. Try again."))

    else:
        change_db_password(new_password)
        flash(escape("Password change successful."))
        return redirect(url_for("main.dashboard"))

    return redirect(url_for("authorize.change_password"))

@authorize.route("/registration_change_password")
def registration_change_password():
    """Establishes route for the change password page for a new user..

    This route is accessible within the email that is sent to new users and
    will be publically accessible.

    Returns:
        Renders change password page for user with their selected language.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]
    return render_template(
        "registration_change_password.html", language=language, translations=translations
    )


@authorize.route("/registration_change_password", methods=["POST"])
def post_registration_change_password():
    """
    """

    email = request.form.get("email").lower()

    temp_password, new_password, new_password_confirm = extract_new_pw_data(
        request.form
    )

     # ensure that input meets requirments
    if not validate_email_syntax(email):
        flash(escape("Please enter a valid email address"))

    # Confirm that email exists as a user
    user = User.query.filter_by(email=email).first()

     # check if the user actually exists & password is correct
    if not user or not verify_password(user.password, temp_password):
        flash(escape("Please check that your email and registration password are correct and try again."))
        return redirect(
            url_for("authorize.registration_change_password")
        )
   
    elif temp_password == new_password:
        # Do not need to check password hash because old password is correct
        flash(
            escape("New password cannot be the same as your previous password.")
        )

    elif not new_password == new_password_confirm:
        flash(escape("New passwords do not match. Try again"))

    elif not validate_password(new_password):
        flash(escape("New password does not meet requirements. Try again."))

    else:
        change_db_password(new_password)
        flash(escape("Password change successful."))
        return redirect(url_for("authorize.register"))

    return redirect(url_for("authorize.registration_change_password"))


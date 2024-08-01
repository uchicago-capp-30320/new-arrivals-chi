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
    * register - Route to the organization's inital register page.
    * post_register - Executes inital organization registration logic.
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
from new_arrivals_chi.app.database import User, Organization
from new_arrivals_chi.app.utils import (
    validate_email_syntax,
    validate_password,
    extract_signup_data,
    extract_new_pw_data,
    verify_password,
    extract_registration_info,
)
from new_arrivals_chi.app.constants import (
    KEY_TRANSLATIONS,
    KEY_LANGUAGE,
    DEFAULT_LANGUAGE,
)
from flask_login import login_user, login_required, logout_user, current_user
from functools import wraps
from new_arrivals_chi.app.data_handler import (
    create_user,
    change_db_password,
    change_organization_status,
    org_registration,
)

import logging

logging.basicConfig(level=logging.INFO)


authorize = Blueprint("authorize", __name__, static_folder="/static")


def admin_required(f):
    """Function so only authed users with admin privileges can access routes.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: Decorated function.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            flash("You are not authorized to access this page.", "error")
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)

    return decorated_function


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
        login_user(new_user)
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
    return render_template(
        "login.html", language=language
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

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists & password is correct
    if not user or not verify_password(user.password, password):
        flash(escape("Please check your login details and try again."))
        return redirect(
            url_for("authorize.login")
        )  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user)

    if current_user.role == "admin":
        return render_template(
            "admin_management.html",

        )
    else:
        organization = Organization.query.get(user.organization_id)
        return render_template(
            "dashboard.html",
            organization=organization,
        )


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
    return render_template(
        "change_password.html", language=language
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
    """Establishes route for the change password page for a new user.

    This route is accessible within the email that is sent to new users and
    will be publically accessible.

    Returns:
        Renders change password page for user with their selected language.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "registration_change_password.html",
        language=language,
        translations=translations,
    )


@authorize.route("/registration_change_password", methods=["POST"])
def post_registration_change_password():
    """Handles the POST request for changing the password for a new user.

    This function processes the form data, validates it, and flashes
    messages to the user in the appropriate language based on their
    selection. If the validation passes, it updates the user's password
    and redirects to the registration page.
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
        flash(escape("Please check your email and registration password."))
        return redirect(url_for("authorize.registration_change_password"))

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
        return redirect(url_for("authorize.register"))

    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]
    return render_template(
        "registration_change_password.html",
        language=language,
        translations=translations,
    )


@authorize.route("/register", methods=["POST"])
@login_required
def post_register():
    """Allows an new authorized user to set up their organization's information.

    Returns:
        Redirects to the organization's dashboard page if password change is
        successful, otherwise redirects back to the registrations page with a
        flash message.
    """
    location, hours = extract_registration_info(request.form)

    if any(value is None for value in location.values()):
        flash(escape("Please confirm that the entered location is correct."))
    elif any(value is None for value in hours.values()):
        flash(escape("Please confirm that the entered hours are correct."))
    else:
        # Add information to the database
        org_registration(location, hours)
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("authorize.register"))


@authorize.route("/register")
@login_required
def register():
    """Establishes route for registering an organizations information.

    This route is accessible once a new user changes their password and logs in.

    Returns:
        Renders register page for user with their selected language.
    """
    language = bleach.clean(request.args.get("lang", "en"))
    translations = current_app.config["TRANSLATIONS"][language]
    return render_template(
        "register.html", language=language, translations=translations
    )


@authorize.route("/admin")
@admin_required
def admin_dashboard():
    """Establishes route to admin management or redirects to home based on user.

    This route checks if the current user is an admin. If yes, it renders
    the admin dashboard template. If not, it redirects the user to the home
    page.

    Returns:
        Renders the admin dashboard page where admin can select to manage
        organizations or look at website error reports. If user is not admin,
        it redirects to home page.
    """

    if current_user.is_admin:
        return render_template(
            "admin_management.html",
        )
    else:
        return render_template(
            "home.html"
        )


@authorize.route("/admin/org_management", methods=["GET"])
@admin_required
def org_management():
    """Establishes route to org management page w/ list of orgs.

    This route fetches a list of organizations from the database and renders
    the organization management template with the list.

    Returns:
        Renders template with organizations.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))

    organizations = Organization.query.with_entities(
        Organization.id, Organization.name, Organization.status
    ).all()

    return render_template(
        "org_management.html",
        organizations=organizations,
        language=language,
    )


@authorize.route(
    "/suspend_organization/<int:organization_id>", methods=["GET", "POST"]
)
@admin_required
def toggle_suspend_organization(organization_id):
    """Establishes route to toggle the status of an organization to suspend it.

    This route suspends an organization by toggling its status. It expects the
    organization_id to be provided in the form data. If the organization is
    successfully suspended, a success message is flashed. If the organization is
    not found or if the request is invalid, appropriate error messages are
    flashed. After processing the request, the user is redirected to the
    org_management page.

    Returns:
        Response: Redirects to org_management page with flashed messages.
    """
    if organization_id:
        updated_organization = change_organization_status(organization_id)
        print(updated_organization)
        if updated_organization:
            flash(
                escape(
                    f"Organization status change to \
                         {updated_organization.status}"
                ),
                "success",
            )
        else:
            flash(escape("Organization not found."), "error")
    else:
        flash(escape("Invalid request."), "error")
    # redirect to org management page in all cases? should i do that?
    return redirect(url_for("authorize.org_management"))


@authorize.route("/admin/edit_organization/<int:organization_id>")
@admin_required
def admin_edit_organization(organization_id):
    """Establishes route to the edit organization page.

    This route is accessible by selecting 'Dashboard' on the
    home page.

    Returns:
        Renders the edit organization page where admin or organizations can
        update their info.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    

    organization = Organization.query.get(organization_id)

    return render_template(
        "edit_organization.html",
        organization_id=organization_id,
        organization=organization,
        language=language,
    )

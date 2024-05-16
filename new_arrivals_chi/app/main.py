"""Project: new_arrivals_chi.

File name: main.py
Associated Files:
    Templates: base.html, home.html, legal.html, health.html,
    health_search.html, profile.html, login.html, info.html.

Runs primary flask application for Chicago's new arrivals' portal.

Methods:
    * home — Route to homepage of application.
    * profile - Route to user's profile.
    * legal - Route to legal portion of application.

Last updated:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/13/2024

Creation:
@Author: Summer Long @Sumslong
@Date: 04/19/2024
"""

from http import HTTPMethod

from flask import Flask, Blueprint, render_template, request, current_app, flash
from markupsafe import escape
import os
import bleach
from dotenv import load_dotenv

from new_arrivals_chi.app.constants import (
    KEY_LANGUAGE,
    KEY_TRANSLATIONS,
    DEFAULT_LANGUAGE,
)
from new_arrivals_chi.app.database import db, User, Organization
from new_arrivals_chi.app.data_handler import create_organization_profile
from new_arrivals_chi.app.utils import load_translations
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user
from new_arrivals_chi.app.authorize_routes import authorize


migrate = Migrate()

load_dotenv()

main = Blueprint("main", __name__, static_folder="/static")


@main.route("/")
def home():
    """Establishes route for the home page of New Arrivals Chi.

    This route is accessible within the 'home' button in the navigation bar and
    is the page that users are directed to when first visiting the site.

    Returns:
        Renders home page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "home.html", language=language, translations=translations
    )


@main.route("/profile", methods=[HTTPMethod.GET, HTTPMethod.POST])
@login_required
def profile():
    """Handles both displaying the user's profile and adding an organization.

    GET: Renders profile page with user's organization info.
    POST: Adds a new organization to the database and redirects to profile page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    if request.method == "POST":
        name = bleach.clean(request.form.get("name"))
        phone = bleach.clean(request.form.get("phone"))
        status = bleach.clean(request.form.get("status"))

        org_id = create_organization_profile(name, phone, status)
        if org_id:
            flash(escape("Organization added successfully."))
        else:
            flash(escape("Failed to add organization."))

    user = current_user
    organization = Organization.query.get(user.organization_id)

    return render_template(
        "profile.html",
        organization=organization,
        translations=translations,
        language=language,
    )


@main.route("/legal")
def legal():
    """Establishes route for the legal page.

    This route is accessible within the 'legal' button on the home page.

    Returns:
        Renders main legal page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "legal_flow.html", language=language, translations=translations
    )


@main.route("/health")
def health():
    """Establishes route for the health page.

    This route is accessible within the 'health' button on the home page.

    Returns:
        Renders main health page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "health.html", language=language, translations=translations
    )


@main.route("/health/search")
def health_search():
    """Establishes route for the health search page.

    This route is accessible by selecting 'Receive Assistance Now' on the
    health page.

    Returns:
        Renders the health search page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "health_search.html", language=language, translations=translations
    )


@main.route("/info")
def info():
    """Establishes route for an unauthenticated view of an org's information.

    This will be accessible when search is implemented.

    Returns:
        Renders information of an organization.
    """
    language = bleach.clean(
        request.args.get(KEY_TRANSLATIONS, DEFAULT_LANGUAGE)
    )
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "info.html", language=language, translations=translations
    )


def create_app(config_override=None):
    """This function creates the flask application for the web portal."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", default="sqlite:///:memory:"
    )
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config[KEY_TRANSLATIONS] = load_translations()

    # Update app configuration with any provided override config (for testing)
    if config_override:
        app.config.update(config_override)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main)
    app.register_blueprint(authorize)

    login_manager = LoginManager()
    login_manager.login_view = "authorize.login"
    login_manager.session_protection = "strong"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


if __name__ == "__main__":
    app = create_app()
    # Note: For the development server, we are using a auto-generated
    # self-signed certificate as a result the CA is unable to validate a server
    # certificate, though you can continue to proceed and visit the development
    # site. For the production deployment, we will ensure a valid certificate
    # from CA for our domain.
    app.run(ssl_context="adhoc", debug=True)

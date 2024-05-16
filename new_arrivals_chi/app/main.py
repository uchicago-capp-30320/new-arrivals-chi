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
from flask_wtf.csrf import CSRFProtect

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
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "legal_flow.html", language=language, translations=translations
    )


@main.route("/legal/tps_info")
def legal_tps_info():
    """Establishes route for the TPS info page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - TPS info page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "tps_info.html", language=language, translations=translations
    )


@main.route("/legal/tps_apply")
def legal_tps_apply():
    """Establishes route for the TPS apply page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - TPS apply page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "tps_apply.html", language=language, translations=translations
    )


@main.route("/legal/vttc_info")
def legal_vttc_info():
    """Establishes route for the VTTC info page.

    This route is accessible within the legal section.

    Returns:
        Renders legal VTTC info page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "vttc_info.html", language=language, translations=translations
    )


@main.route("/legal/vttc_apply")
def legal_vttc_apply():
    """Establishes route for the VTTC apply page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - VTTC apply page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "vttc_apply.html", language=language, translations=translations
    )


@main.route("/legal/asylum_info")
def legal_asylum_info():
    """Establishes route for the Asylum info page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - Asylum info page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "asylum_info.html", language=language, translations=translations
    )


@main.route("/legal/asylum_apply")
def legal_asylum_apply():
    """Establishes route for the Asylum apply page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - Asylum apply page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "asylum_apply.html", language=language, translations=translations
    )


@main.route("/legal/parole_info")
def legal_parole_info():
    """Establishes route for the Parole info page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - Parole info page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "parole_info.html", language=language, translations=translations
    )


@main.route("/legal/parole_apply")
def legal_parole_apply():
    """Establishes route for the Parole apply page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - Parole apply page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "parole_apply.html", language=language, translations=translations
    )


@main.route("/legal/undocumented_resources")
def legal_undocumented_resources():
    """Establishes route for the Undocumented Resources page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - Undocumented Resources page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "undocumented_resources.html",
        language=language,
        translations=translations,
    )


@main.route("/legal/help")
def legal_help():
    """Establishes route for the Legal Help page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - Legal Help page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "help.html", language=language, translations=translations
    )


@main.route("/legal/work_rights")
def workers_rights():
    """Route for information about workers' rights.

    Returns:
        Renders the workers' rights page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "work_rights.html", language=language, translations=translations
    )


@main.route("/legal/renters_rights")
def renters_rights():
    """Route for information about renters' rights.

    Returns:
        Renders the renters' rights page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "renters_rights.html", language=language, translations=translations
    )


@main.route("/legal/general")
def legal_general():
    """Route for general legal information.

    Returns:
        Renders the legal general page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "general.html", language=language, translations=translations
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
    app.config["WTF_CSRF_ENABLED"] = True

    # Update app configuration with any provided override config (for testing)
    if config_override:
        app.config.update(config_override)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main)
    app.register_blueprint(authorize)

    CSRFProtect(app)

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

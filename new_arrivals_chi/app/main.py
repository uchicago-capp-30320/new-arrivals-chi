"""Project: new_arrivals_chi.

File name: main.py
Associated Files:
    Templates: base.html, home.html, legal.html, health.html,
    health_search.html, dashboard.html, login.html, info.html.

Runs primary flask application for Chicago's new arrivals' portal.

Methods:
    * home — Route to homepage of application.
    * dashboard - Route to user's dashboard.
    * legal - Route to legal portion of application.

Last updated:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/13/2024

Creation:
@Author: Summer Long @Sumslong
@Date: 04/19/2024
"""

from flask import (
    Flask,
    Blueprint,
    render_template,
    request,
    current_app,
    url_for,
    flash,
)
import os
import bleach
from markupsafe import escape
from dotenv import load_dotenv

from new_arrivals_chi.app.constants import (
    KEY_LANGUAGE,
    KEY_TRANSLATIONS,
    DEFAULT_LANGUAGE,
)
from new_arrivals_chi.app.database import db, User, Organization
from new_arrivals_chi.app.utils import load_translations
from flask_migrate import Migrate
import sqlite3
from flask_login import LoginManager, login_required, current_user
from new_arrivals_chi.app.authorize_routes import authorize
from datetime import timedelta

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
    # Implementation with demonstrative data
    conn = sqlite3.connect("instance/test_fake_data.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT s.service, l.neighborhood, o.name, "
        + "strftime('%I:%M %p', h.opening_time) "
        "|| ' - ' || "
        "strftime('%I:%M %p', h.closing_time) "
        "AS opening_closing_time "
        "FROM organizations o "
        "JOIN hours h ON o.hours_id = h.id "
        "JOIN locations l ON o.location_id = l.id "
        "JOIN organizations_services os ON o.id = os.organization_id "
        "JOIN services s ON os.service_id = s.id"
    )

    services_info = cursor.fetchall()

    conn.close()

    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "health_search.html",
        language=language,
        translations=translations,
        services_info=services_info,
        set=set,
    )


@main.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    """Establishes route to the organization dashboard.

    This route is accessible by selecting 'Dashboard' on the
    home page.

    Returns:
        Renders the dashboard page with buttons to view org page, edit org page
        and change password.
    """
    language = bleach.clean(request.args.get("lang", "en"))
    translations = current_app.config["TRANSLATIONS"][language]
    user = current_user
    organization = Organization.query.get(user.organization_id)
    if not organization:
        return "Organization not found", 404

    # generate URL for edit_organization endpoint
    edit_org_url = url_for(
        "main.edit_organization", org_name=organization.name, lang=language
    )

    return render_template(
        "dashboard.html",
        organization=organization,
        language=language,
        translations=translations,
        edit_org_url=edit_org_url,
    )


@main.route("/org", methods=["GET"])
@login_required
def org():
    """Establishes route to the organization page.

    This page is dynamically generated based on the org id and contains
    organization details. It is accessible from the org dashboard and the health
    filterable table.

    Returns:
        Renders the organization page (public facing).
    """
    language = bleach.clean(request.args.get("lang", "en"))
    translations = current_app.config["TRANSLATIONS"][language]
    user = current_user
    organization = User.query.get(user.organization_id)
    return render_template(
        "organization.html",
        organization=organization,
        language=language,
        translations=translations,
    )


@main.route("/edit_organization", methods=["GET", "POST"])
@login_required
def edit_organization():
    """Establishes route to the edit organization page.

    This route is accessible by selecting 'Dashboard' on the
    home page.

    Returns:
        Renders the edit organization page where admin or organizations can
        update their info.
    """
    language = bleach.clean(request.args.get("lang", "en"))
    translations = current_app.config["TRANSLATIONS"][language]
    user = current_user
    organization = User.query.get(user.organization_id)
    if request.method == "POST":
        # Handle the form submission
        pass
    return render_template(
        "edit_organization.html",
        organization=organization,
        language=language,
        translations=translations,
    )


@main.route("/add_organization", methods=["GET"])
@login_required
def add_organization():
    """Establishes route to the add organization page.

    This route is accessible by selecting 'Dashboard' on the
    home page.

    Returns:
        Renders the add organization page where admin can add
        a new organization.
    """
    # Check if the user is an admin
    if not current_user.is_admin:
        return "Unauthorized", 401

    language = bleach.clean(request.args.get("lang", "en"))
    translations = current_app.config["TRANSLATIONS"][language]
    if request.method == "POST":
        email = request.form.get("email")
        confirmed_email = request.form.get("email-confirm")

        # Check if the email and confirmed email match
        if email != confirmed_email:
            flash(escape("Emails do not match. Try again"))
        # Handle the form submission
        pass

    return render_template(
        "add_organization.html",
        language=language,
        translations=translations,
    )


def create_app(config_override=None):
    """This function creates the flask application for the web portal."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", default="sqlite:///:memory:"
    )
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(hours=12)
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

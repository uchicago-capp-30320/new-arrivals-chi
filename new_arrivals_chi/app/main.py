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
@Author: Summer Long @Sumslong
@Date: 05/03/2024

Creation:
@Author: Summer Long @Sumslong
@Date: 04/19/2024
"""

from flask import Flask, Blueprint, render_template, request, current_app
import os
import bleach
from dotenv import load_dotenv
from new_arrivals_chi.app.database import db, User
from new_arrivals_chi.app.utils import load_translations
from flask_migrate import Migrate
from flask_login import LoginManager, login_required
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
    language = bleach.clean(request.args.get("lang", "en"))
    translations = current_app.config["TRANSLATIONS"][language]

    return render_template(
        "home.html", language=language, translations=translations
    )


@main.route("/profile")
@login_required
def profile():
    """Establishes route for the user's profile page.

    This route is accessible within the 'profile' button in the navigation bar.

    Returns:
        Renders profile page for user with in their selected language.
    """
    language = bleach.clean(request.args.get("lang", "en"))
    translations = current_app.config["TRANSLATIONS"][language]

    return render_template(
        "profile.html", language=language, translations=translations
    )


@main.route("/legal")
def legal():
    """Establishes route for the legal page.

    This route is accessible within the 'legal' button on the home page.

    Returns:
        Renders main legal page.
    """
    language = bleach.clean(request.args.get("lang", "en"))

    translations = app.config["TRANSLATIONS"][language]

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
    language = bleach.clean(request.args.get("lang", "en"))

    translations = app.config["TRANSLATIONS"][language]

    return render_template(
        "legal_tps_info.html", language=language, translations=translations
    )


@main.route("/legal/tps_apply")
def legal_tps_apply():
    """Establishes route for the TPS apply page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - TPS apply page.
    """
    language = bleach.clean(request.args.get("lang", "en"))

    translations = app.config["TRANSLATIONS"][language]

    return render_template(
        "legal_tps_apply.html", language=language, translations=translations
    )


@main.route("/legal/vttc_info")
def legal_vttc_info():
    """Establishes route for the VTTC info page.

    This route is accessible within the legal section.

    Returns:
        Renders legal VTTC info page.
    """
    language = bleach.clean(request.args.get("lang", "en"))

    translations = app.config["TRANSLATIONS"][language]

    return render_template(
        "legal_vttc_info.html", language=language, translations=translations
    )


@main.route("/legal/vttc_apply")
def legal_vttc_apply():
    """Establishes route for the VTTC apply page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - VTTC apply page.
    """
    language = bleach.clean(request.args.get("lang", "en"))

    translations = app.config["TRANSLATIONS"][language]

    return render_template(
        "legal_vttc_apply.html", language=language, translations=translations
    )


@main.route("/legal/asylum_info")
def legal_asylum_info():
    """Establishes route for the Asylum info page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - Asylum info page.
    """
    language = bleach.clean(request.args.get("lang", "en"))

    translations = app.config["TRANSLATIONS"][language]

    return render_template(
        "legal_asylum_info.html", language=language, translations=translations
    )


@main.route("/legal/asylum_apply")
def legal_asylum_apply():
    """Establishes route for the Asylum apply page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - Asylum apply page.
    """
    language = bleach.clean(request.args.get("lang", "en"))

    translations = app.config["TRANSLATIONS"][language]

    return render_template(
        "legal_asylum_apply.html", language=language, translations=translations
    )


@main.route("/legal/parole_info")
def legal_parole_info():
    """Establishes route for the Parole info page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - Parole info page.
    """
    language = bleach.clean(request.args.get("lang", "en"))
    translations = app.config["TRANSLATIONS"][language]

    return render_template(
        "legal_parole_info.html", language=language, translations=translations
        )


@main.route("/legal/parole_apply")
def legal_parole_apply():
    """Establishes route for the Parole apply page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - Parole apply page.
    """
    language = bleach.clean(request.args.get("lang", "en"))
    translations = app.config["TRANSLATIONS"][language]

    return render_template(
        "legal_parole_apply.html", language=language, translations=translations
        )


@main.route("/legal/undocumented_resources")
def legal_undocumented_resources():
    """Establishes route for the Undocumented Resources page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - Undocumented Resources page.
    """
    language = bleach.clean(request.args.get("lang", "en"))
    translations = app.config["TRANSLATIONS"][language]

    return render_template(
        "undocumented_resources.html", language=language, \
            translations=translations)


@main.route("/legal/legal_help")
def legal_legal_help():
    """Establishes route for the Legal Help page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - Legal Help page.
    """
    language = bleach.clean(request.args.get("lang", "en"))
    translations = app.config["TRANSLATIONS"][language]

    return render_template(
        "legal_help.html", language=language, translations=translations
        )


@main.route("/health")
def health():
    """Establishes route for the health page.

    This route is accessible within the 'health' button on the home page.

    Returns:
        Renders main health page.
    """
    language = bleach.clean(request.args.get("lang", "en"))
    translations = current_app.config["TRANSLATIONS"][language]

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
    language = bleach.clean(request.args.get("lang", "en"))
    translations = current_app.config["TRANSLATIONS"][language]

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
    language = bleach.clean(request.args.get("lang", "en"))
    translations = current_app.config["TRANSLATIONS"][language]

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
    app.config["TRANSLATIONS"] = load_translations()

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
    app.run(ssl_context=("adhoc"), debug=True)

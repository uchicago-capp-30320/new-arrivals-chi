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
"""

from flask import Flask, Blueprint, render_template, request, g, flash
from flask_babel import Babel, lazy_gettext as _
from datetime import timedelta
import os
from new_arrivals_chi.app.authorize_routes import authorize
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_required
import bleach
from markupsafe import escape
from new_arrivals_chi.app.utils import (
    load_neighborhoods,
    validate_email_syntax,
    validate_phone_number,
    create_temp_pwd,
)
from new_arrivals_chi.app.data_handler import (
    create_user,
    create_organization_profile,
    extract_organization,
)
from dotenv import load_dotenv
from new_arrivals_chi.app.database import (
    db,
    User,
    Organization,
)
from new_arrivals_chi.app.constants import KEY_LANGUAGE, DEFAULT_LANGUAGE

migrate = Migrate()
load_dotenv()

app = Flask(__name__)
babel = Babel(app)


def get_locale():
    """Get the current locale based on the request."""
    lang = request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE)
    g.current_lang = lang
    return lang


babel.init_app(app, locale_selector=get_locale)


@app.context_processor
def inject_locale():
    """Inject the current locale into the context."""
    return {"get_locale": get_locale}


# Define the blueprint
main = Blueprint("main", __name__, static_folder="static")


# Define routes within the blueprint
@main.route("/")
def home():
    """Home page route."""
    return render_template("home.html")


@main.route("/about")
def about():
    """About page route."""
    return render_template("about.html")


# Define other routes similarly within the `main` blueprint
@main.route("/legal")
def legal():
    """Establishes route for the legal page.

    This route is accessible within the 'legal' button on the home page.

    Returns:
        Renders main legal page.
    """
    legal_text = {
        "asylum": _(
            "I have a credible fear of persecution or torture in my home "
            "country."
        ),
        "asylum_apply": _("I want help applying for asylum."),
        "asylum_header": _("We think you may be eligible for asylum."),
        "asylum_info": _("I have applied for or received asylum."),
        "hide_options": _("Hide Options"),
        "lawyers": _("Find Personalized Legal Assistance."),
        "other": _("None of these apply to me."),
        "other_header": _(
            "We cannot determine your eligibility for Asylum, Parole, or "
            "Temporary Protected Status"
        ),
        "parole": _("One of the circumstances below applies to me."),
        "parole_apply": _("I want help applying for humanitarian parole."),
        "parole_desc": _(
            "I am from Ukraine or Afghanistan\nI am from Cuba, Haiti, "
            "Nicaragua, and Venezuela and am experiencing dangerous "
            "conditions, violence, or severe economic hardship in my home "
            "country\nI came to the US for Medical Family Reunification "
            "(adults and children)\n I came to the US for Civil or Criminal "
            "Court Proceedings"
        ),
        "parole_header": _(
            "We think you may be eligible for humanitarian parole."
        ),
        "parole_info": _("I have applied for or received humanitarian parole."),
        "renters_rights": _("I need to learn more about my rights as a renter"),
        "see_options": _("See Options"),
        "something_else": _("I need help with something else"),
        "tps": _(
            "I am from one of the countries listed below & arrived before "
            "the date listed:"
        ),
        "tps_apply": _(
            "I want help applying for Temporary Protected Status (TPS)"
        ),
        "tps_desc": _(
            "Afghanistan (May 20, 2022)\nBurma (Myanmar) (March 25, 2024)\n"
            "Cameroon (June 7, 2022)\nEl Salvador (December 14, 2023)\n"
            "Ethiopia (April 15, 2024)\nHaiti (December 14, 2023)\nHonduras "
            "(December 14, 2023)\nNepal (December 14, 2023)\nNicaragua "
            "(December 14, 2023)\nSomalia (March 13, 2023)\nSouth Sudan "
            "(August 21, 2023)\nSudan (December 14, 2023)\nSyria (January 29, "
            "2024)\nUkraine (August 21, 2023)\nVenezuela (November 17, 2023)\n"
            "Yemen (January 3, 2023)"
        ),
        "tps_header": _(
            "We think you may be eligible for Temporary Protected Status "
            "(TPS)"
        ),
        "tps_info": _(
            "I have applied for or received Temporary Protected Status (TPS)"
        ),
        "undocumented": _(
            "Learn more about resources for undocumented migrants."
        ),
        "vttc": _("I am the victim of one of the following:"),
        "vttc_apply": _("I want help applying for work authorization."),
        "vttc_desc": _(
            "Trafficking\nDomestic violence\nSexual assault\nHate crimes\n"
            "Human trafficking\nInvoluntary servitude\nAnother Serious Offense."
        ),
        "vttc_header": _(
            "We think you may be eligible for work authorization."
        ),
        "vttc_info": _("I have applied for or received work authorization."),
        "what_help": _("What can I help you with?"),
        "work_auth": _("I need help getting authorization to work"),
        "work_auth_question": _(
            "Do any of the following circumstances apply to you?"
        ),
        "work_rights": _("I need to learn more about my rights as a worker"),
    }
    return render_template("legal_flow.html", legal_text=legal_text)


@main.route("/legal/tps_info")
def legal_tps_info():
    """Establishes route for the TPS info page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - TPS info page.
    """
    return render_template("tps_info.html")


@main.route("/legal/tps_apply")
def legal_tps_apply():
    """Establishes route for the TPS apply page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - TPS apply page.
    """
    return render_template("tps_apply.html")


@main.route("/legal/vttc_info")
def legal_vttc_info():
    """Establishes route for the VTTC info page.

    This route is accessible within the legal section.

    Returns:
        Renders legal VTTC info page.
    """
    return render_template("vttc_info.html")


@main.route("/legal/vttc_apply")
def legal_vttc_apply():
    """Establishes route for the VTTC apply page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - VTTC apply page.
    """
    return render_template("vttc_apply.html")


@main.route("/legal/asylum_info")
def legal_asylum_info():
    """Establishes route for the Asylum info page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - Asylum info page.
    """
    return render_template("asylum_info.html")


@main.route("/legal/asylum_apply")
def legal_asylum_apply():
    """Establishes route for the Asylum apply page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - Asylum apply page.
    """
    return render_template("asylum_apply.html")


@main.route("/legal/parole_info")
def legal_parole_info():
    """Establishes route for the Parole info page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - Parole info page.
    """
    return render_template("parole_info.html")


@main.route("/legal/parole_apply")
def legal_parole_apply():
    """Establishes route for the Parole apply page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - Parole apply page.
    """
    return render_template("parole_apply.html")


@main.route("/legal/undocumented_resources")
def legal_undocumented_resources():
    """Establishes route for the Undocumented Resources page.

    This route is accessible within the legal section.

    Returns:
        Renders legal flow - Undocumented Resources page.
    """
    return render_template("undocumented_resources.html")


@main.route("/legal/work_rights")
def workers_rights():
    """Route for information about workers' rights.

    Returns:
        Renders the workers' rights page.
    """
    return render_template("work_rights.html")


@main.route("/legal/renters_rights")
def renters_rights():
    """Route for information about renters' rights.

    Returns:
        Renders the renters' rights page.
    """
    return render_template("renters_rights.html")


@main.route("/legal/lawyers")
def lawyers():
    """Route for lawyers.

    Returns:
        Renders the page with contact information for lawyers
    """
    return render_template("lawyers.html")


@main.route("/health")
def health():
    """Establishes route for the health page.

    This route is accessible within the 'health' button on the home page.

    Returns:
        Renders main health page.
    """
    return render_template("health.html")


@main.route("/health/search")
def health_search():
    """Establishes route for the health search page.

    This route is accessible by selecting 'Receive Assistance Now' on the
    health page.

    Returns:
        Renders the health search page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))

    organizations = []

    organization_ids = (
        db.session.query(Organization.id)
        .filter(Organization.location_id.isnot(None))
        .all()
    )

    for org_id in organization_ids:
        if extract_organization(org_id[0])["service"]:
            organizations.append(extract_organization(org_id[0]))

    return render_template(
        "health_search.html",
        services_info=organizations,
        set=set,
        language=language,
    )


@main.route("/health_general")
def health_general():
    """Route for general health static page.

    Returns:
        Health Static Page
    """
    language = request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE)
    return render_template("health_general.html", language=language)


@main.route("/general")
def general():
    """Route for Chicago 101 page.

    Returns:
        Chicago 101 page
    """
    return render_template("general.html")


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
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    user = current_user

    if current_user.role == "admin":
        return render_template(
            "admin_management.html",
            language=language,
        )
    else:
        organization = Organization.query.get(user.organization_id)

        if not organization:
            return "Organization not found", 404

        return render_template(
            "dashboard.html",
            language=language,
            organization=organization,
        )


@main.route("/org/<int:organization_id>", methods=["GET"])
def org(organization_id):
    """Establishes route to the organization page.

    This page is dynamically generated based on the org id and contains
    organization details. It is accessible from the org dashboard.

    Returns:
        Renders the organization page (public facing).
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))

    organization = extract_organization(organization_id)

    return render_template(
        "organization.html",
        organization=organization,
        language=language,
        organization_id=organization_id,
    )


@main.route("/edit_organization/<int:organization_id>", methods=["GET"])
@login_required
def edit_organization(organization_id):
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


@main.route("/add_organization_success", methods=["GET"])
@login_required
def add_organization_success():
    """Establishes route to the add organization success page.

    This route is accessible by selecting 'Dashboard' on the
    home page.

    Returns:
        Renders the add organization success page where admin can view
        a success message after adding a new organization.
    """
    language = bleach.clean(request.args.get("lang", "en"))
    return render_template(
        "add_organization_success.html",
        language=language,
    )


@main.route("/add_organization", methods=["GET", "POST"])
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
    if current_user.role != "admin":
        return "Unauthorized", 401

    language = bleach.clean(request.args.get("lang", "en"))

    if request.method == "POST":
        email = request.form.get("email")
        confirmed_email = request.form.get("email-confirm")
        phone_number = request.form.get("phone-number")
        org_name = request.form.get("org-name")

        # Check if the email and confirmed email match
        if email != confirmed_email:
            flash(escape("Emails do not match. Try again"))
        # Handle the form submission
        elif not validate_email_syntax(email):
            flash(escape("Invalid email address. Try again"))

        elif not validate_phone_number(phone_number):
            flash(
                escape("Invalid phone number (correct example: ###-###-####)")
            )
        else:
            # Create the organization as HIDDEN
            new_org_id = create_organization_profile(
                org_name, phone_number, "HIDDEN"
            )

            # Create a temporary password for the user
            temp_pwd = create_temp_pwd(email, phone_number)

            # Create the user with the provided email and a default password
            new_user = create_user(email, temp_pwd)

            # Update the user with the new organization
            try:
                user = User.query.get(new_user.id)
                user.organization_id = new_org_id
                db.session.commit()
            except Exception as error:
                print(f"Error updating user with organization: {error}")

            # Redirect to the success page
            return render_template(
                "add_organization_success.html",
                language=language,
            )

    return render_template(
        "add_organization.html",
        language=language,
    )


# Function to create the Flask app
def create_app(config_override=None):
    """Function to create the Flask app.

    Args:
        config_override (dict, optional):
          Configuration settings to override defaults. Defaults to None.

    Returns:
        Flask: Configured Flask application instance.
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", default="sqlite:///:memory:"
    )
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(hours=12)

    # Load neighborhoods from file and store in app config
    app.config["NEIGHBORHOODS"] = load_neighborhoods()

    # Configure Babel
    app.config["BABEL_DEFAULT_LOCALE"] = "en"
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "../translations"

    @app.context_processor
    def inject_locale():
        return {"get_locale": get_locale}

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


# Run the Flask app with the correct entry point
if __name__ == "__main__":
    app = create_app()
    app.run(ssl_context="adhoc", debug=True)

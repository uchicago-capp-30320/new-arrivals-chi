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

from flask import (
    Flask,
    Blueprint,
    render_template,
    request,
    current_app,
    flash,
    url_for,
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

from new_arrivals_chi.app.database import (
    db,
    User,
    Organization,
    Language,
    Hours,
    Service,
    Location,
    organizations_services,
    organizations_hours,
    languages_organizations,
)
from new_arrivals_chi.app.utils import (
    load_translations,
    load_neighborhoods,
    validate_email_syntax,
    validate_phone_number,
    validate_city,
    validate_zip_code,
    validate_state,
    validate_street,
    create_temp_pwd,
)

from new_arrivals_chi.app.data_handler import (
    create_user,
    create_organization_profile,
)

from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user
from new_arrivals_chi.app.authorize_routes import authorize
from datetime import timedelta
from sqlalchemy import select, join

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


@main.route("/about")
def about():
    """Establishes route for the about us page.

    This route is accessible from the footer of every page.

    Returns:
        Renders about us page.
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "about.html", language=language, translations=translations
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


@main.route("/legal/lawyers")
def lawyers():
    """Route for lawyers.

    Returns:
        Renders the page with contact information for lawyers
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "lawyers.html", language=language, translations=translations
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

    stmt = select(
        Service.service,
        Location.neighborhood,
        Organization.name,
        Organization.id,
        db.func.concat(
            db.func.to_char(Hours.opening_time, "HH:MI AM"),
            " - ",
            db.func.to_char(Hours.closing_time, "HH:MI AM"),
        ).label("opening_closing_time"),
    ).select_from(
        join(
            Organization,
            organizations_hours,
            Organization.id == organizations_hours.c.organization_id,
        )
        .join(Hours, organizations_hours.c.hours_id == Hours.id)
        .join(Location, Organization.location_id == Location.id)
        .join(
            organizations_services,
            Organization.id == organizations_services.c.organization_id,
        )
        .join(Service, organizations_services.c.service_id == Service.id)
    )

    services_info = db.session.execute(stmt).fetchall()

    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]
    return render_template(
        "health_search.html",
        language=language,
        translations=translations,
        services_info=services_info,
        set=set,
    )


@main.route("/health_general")
def health_general():
    """Route for general health static page.

    Returns:
        Health Static Page
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "health_general.html", language=language, translations=translations
    )


@main.route("/general")
def general():
    """Route for Chicago 101 page.

    Returns:
        Chicago 101 page
    """
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]

    return render_template(
        "general.html", language=language, translations=translations
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
    language = bleach.clean(request.args.get(KEY_LANGUAGE, DEFAULT_LANGUAGE))
    translations = current_app.config[KEY_TRANSLATIONS][language]
    user = current_user

    if current_user.role == "admin":
        return render_template(
            "admin_management.html",
            language=language,
            translations=translations,
        )
    else:
        organization = Organization.query.get(user.organization_id)

        if not organization:
            return "Organization not found", 404

        # generate URL for edit_organization endpoint
        edit_org_url = url_for(
            "main.edit_organization",
            organization_id=organization.id,
            lang=language,
        )

        return render_template(
            "dashboard.html",
            language=language,
            organization=organization,
            translations=translations,
            edit_org_url=edit_org_url,
        )


@main.route("/org/<int:organization_id>", methods=["GET"])
def org(organization_id):
    """Establishes route to the organization page.

    This page is dynamically generated based on the org id and contains
    organization details. It is accessible from the org dashboard.

    Returns:
        Renders the organization page (public facing).
    """
    print(f"Hi, {organization_id}")
    stmt = (
        select(
            Organization.name,
            Location.street_address,
            Organization.phone,
            Language.language,
            Service.service,
            db.func.concat(
                db.func.to_char(Hours.opening_time, "HH:MI AM"),
                " - ",
                db.func.to_char(Hours.closing_time, "HH:MI AM"),
            ).label("opening_closing_time"),
        )
        .select_from(
            join(
                Organization,
                organizations_hours,
                Organization.id == organizations_hours.c.organization_id,
            )
            .join(Hours, organizations_hours.c.hours_id == Hours.id)
            .join(Location, Organization.location_id == Location.id)
            .join(
                organizations_services,
                Organization.id == organizations_services.c.organization_id,
            )
            .join(Service, organizations_services.c.service_id == Service.id)
            .join(
                languages_organizations,
                Organization.id == languages_organizations.c.organization_id,
            )
            .join(
                Language, languages_organizations.c.language_id == Language.id
            )
        )
        .where(Organization.id == organization_id)
    )

    organization_info = db.session.execute(stmt).fetchall()

    language = bleach.clean(request.args.get("lang", "en"))
    translations = current_app.config["TRANSLATIONS"][language]

    if organization_info:
        organization = {
            "name": organization_info[0][0],
            "address": organization_info[0][1],
            "phone": organization_info[0][2],
            "language": organization_info[0][3],
            "service": (", ").join({info[4] for info in organization_info}),
            "hours": organization_info[0][5],
        }

    language = bleach.clean(request.args.get("lang", "en"))
    translations = current_app.config["TRANSLATIONS"][language]

    return render_template(
        "organization.html",
        organization_id=organization_id,
        organization=organization,
        language=language,
        translations=translations,
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
    translations = current_app.config[KEY_TRANSLATIONS][language]
    user = current_user

    # if user.role == "admin":
    #     # Query DB to get the organization's Data
    #     # organzation id is the one in the url
    #     organization_id = bleach(request.args.get("organization_id"))
    #     organization = Organization.query.get(organization_id)

    # else:
    organization = User.query.get(user.organization_id)

    # organization = User.query.get(user.organization_id)
    if request.method == "POST":
        # Handle the form submission
        pass
    return render_template(
        "edit_organization.html",
        organization=organization,
        language=language,
        translations=translations,
        organization_id=organization_id,
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
    translations = current_app.config["TRANSLATIONS"][language]
    return render_template(
        "add_organization_success.html",
        language=language,
        translations=translations,
    )


@main.route("/edit_location", methods=["POST"])
@login_required
def edit_location():
    """POST request to edit the organization's location.

    Parameters
    ----------
    organization_id : int
        The organization's id.
    """
    street_address = request.form.get("street_address")
    city = request.form.get("city")
    state = request.form.get("state")
    zip_code = request.form.get("zip-code")
    neighborhood = request.form.get("neighborhood")
    primary_location = request.form.get("primary_location")

    # Get user's current organization
    user = current_user
    organization = Organization.query.get(user.organization_id)

    location = Location.query.get(organization.location_id)
    location.street_address = street_address
    location.city = city
    location.state = state
    location.zip_code = zip_code
    location.neighborhood = neighborhood
    location.primary_location = primary_location

    if not validate_street(street_address):
        flash(escape("Invalid street address. Try again"))

    elif not validate_city(city):
        flash(escape("Invalid city. Try again"))

    elif not validate_state(state):
        flash(escape("Invalid state. Try again"))

    elif not validate_zip_code(zip_code):
        flash(escape("Invalid zip code. Try again"))

    else:
        # Update the organization's location
        try:
            db.session.commit()

        except Exception as error:
            print(f"Error updating location: {error}")


@main.route("/edit_contact_info", methods=["POST"])
@login_required
def edit_contact_info():
    """POST request to edit the organization's contact information.

    Parameters
    ----------
    organization_id : int
        The organization's id.
    """
    phone_number = request.form.get("phone-number")
    email = request.form.get("email")

    # Get user's current organization
    user = current_user
    organization = Organization.query.get(user.organization_id)

    organization.phone = phone_number
    user.email = email

    if not validate_email_syntax(email):
        flash(escape("Invalid email address. Try again"))

    elif not validate_phone_number(phone_number):
        flash(escape("Invalid phone number. Try again"))

    else:
        # Update the organization's contact information
        try:
            db.session.commit()

        except Exception as error:
            print(f"Error updating contact information: {error}")


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
    translations = current_app.config["TRANSLATIONS"][language]

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
                translations=translations,
            )

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

    # Load neighborhoods from file and store in app config
    app.config["NEIGHBORHOODS"] = load_neighborhoods()

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


def retrieve_hours(all_hours):
    # Retrieve all opperating hours
    organization_hours = {
        "monday": [],
        "tuesday": [],
        "wednesday": [],
        "thursday": [],
        "friday": [],
        "saturday": [],
        "sunday": [],
    }

    weekdays = {
        1: "monday",
        2: "tuesday",
        3: "wednesday",
        4: "thursday",
        5: "friday",
        6: "saturday",
        7: "sunday",
    }

    for current_hour in all_hours:
        extract_hour_info(current_hour, organization_hours, weekdays)

    return organization_hours


def extract_organization():
    user_info = User.query.filter_by(id=current_user.id).first()
    org_info = Organization.query.filter_by(
        id=current_user.organization_id
    ).first()
    primary_location_info = Location.query.filter_by(
        id=org_info.location_id
    ).first()

    # Retrieve all opperating hours
    language_list = retrieve_languages(org_info)

    # Retrieve all opperating hours
    organization_hours = retrieve_hours(org_info.hours)

    # Retrieve services and associated locations
    complete_service_info = retrieve_services(org_info.services)

    organization = {
        "name": org_info.name,
        "phone": org_info.phone,
        "email": user_info.email,
        "language": language_list,
        "service": complete_service_info,
        "hours": organization_hours,
        # Primary location information
        "street_address": primary_location_info.street_address,
        "zip_code": primary_location_info.zip_code,
        "city": primary_location_info.city,
        "state": primary_location_info.state,
        "primary_location": primary_location_info.primary_location,
        "neighborhood": primary_location_info.neighborhood,
    }

    return organization


def extract_hour_info(current_hour, organization_hours, weekdays):
    day = current_hour.day_of_week
    day_str = weekdays[day]
    associated_hours = {
        "open": current_hour.opening_time,
        "close": current_hour.closing_time,
    }

    # Ensure the ordering of hours are correct
    if not organization_hours[day_str]:
        organization_hours[day_str].append(associated_hours)
    else:
        # Check existing entries and insert based on opening time
        inserted = False
        for i, existing_hours in enumerate(organization_hours[day_str]):
            if current_hour.opening_time < existing_hours["open"]:
                organization_hours[day_str].insert(i, associated_hours)
                inserted = True
                break
        if not inserted:
            organization_hours[day_str].append(associated_hours)


def retrieve_languages(org_reference):
    all_languages = org_reference.languages
    language_list = []
    for curr_language in all_languages:
        language_list.append(curr_language.language)


def retrieve_services(all_services):
    complete_service_info = []
    for curr_service in all_services:
        service_info = {
            "category": curr_service.category,
            "service": curr_service.service,
            "access": curr_service.access,
            "service_note": curr_service.service_note,
            "dates": retrieve_dates(curr_service.service_dates),
            "locations": retrieve_locations(curr_service.locations),
        }
        complete_service_info.append(service_info)

    return complete_service_info


def retrieve_dates(all_dates):
    complete_date_info = []

    # Retrieve all dates for service
    for current_date in all_dates:
        complete_date_info.append(extract_date_info(current_date))

    return complete_date_info


def extract_date_info(current_date):
    single_date_info = {
        "date": current_date.date,
        "start_time": current_date.start_time,
        "end_time": current_date.end_time,
        "repeat": current_date.repeat,
    }
    return single_date_info


def retrieve_locations(all_locations):
    complete_location_info = []

    # Retrieve all dates for service
    for current_location in all_locations:
        complete_location_info.append(extract_location_info(current_location))

    return complete_location_info


def extract_location_info(current_location):
    pass


if __name__ == "__main__":
    app = create_app()
    # Note: For the development server, we are using a auto-generated
    # self-signed certificate as a result the CA is unable to validate a server
    # certificate, though you can continue to proceed and visit the development
    # site. For the production deployment, we will ensure a valid certificate
    # from CA for our domain.
    app.run(ssl_context="adhoc", debug=True)

"""Project: new_arrivals_chi.

File name: data_handler.py
Associated Files:
   authorize_routes.py.

This file contains utility methods for validating user input and handling
database operations.

Methods:
    * create_user - Creates a new user in the database.
    * change_db_password - Changes the password for the current user in the
      database.
    * create_organization_profile - Creates an organization in the database.
    * org_registration - Registers an organization's location and hours.
    * add_location - Adds a new location to the database.
    * add_hours - Adds new operating hours to the database.
    * assign_location_foreign_key_org_table - Assigns a location ID to
      an organization.
    * change_organization_status - Changes the status of an organization in the
      database.
    * extract_organization - Extracts detailed information about an
      organization.
    * retrieve_hours - Retrieves the operating hours for an organization.
    * extract_hour_info - Extracts and organizes hour information for a
      specific day.
    * retrieve_languages - Retrieves all languages spoken at an organization.
    * retrieve_services - Retrieves detailed information about the services
      offered by an organization.
    * retrieve_dates - Retrieves all dates associated with a service.
    * extract_date_info - Extracts detailed information about a specific date.
    * retrieve_locations - Retrieves all location details associated with a
      service.
    * extract_location_info - Extracts detailed information about a specific
      location.
"""

from new_arrivals_chi.app.database import (
    db,
    User,
    Organization,
    Location,
    Hours,
    organizations_hours,
)
from flask_login import current_user
from flask_bcrypt import Bcrypt
from sqlalchemy import insert


bcrypt = Bcrypt()


def create_user(email, password):
    """Creates a new user in the database.

    Parameters:
        email (str): The email address of the new user.
        password (str): The password of the new user.

    Returns:
        User: The newly created User object.
    """
    new_user = User(
        email=email,
        password=bcrypt.generate_password_hash(password).decode("utf-8"),
    )
    db.session.add(new_user)
    db.session.commit()

    return new_user


def change_db_password(password):
    """Changes the password for the current user in the database.

    Parameters:
        password (str): The new password for the current user.
    """
    current_user.password = bcrypt.generate_password_hash(password).decode(
        "utf-8"
    )
    db.session.commit()


def create_organization_profile(name, phone, status):
    """Create new organization in the database.

    Create a new organization with the required (non-nullable) organization
    details.

    Parameters:
        name (str): Name of organization.
        phone (str): Primary external contact number for the organization.
        status (str): Indicates the organization's status eg: ACTIVE, HIDDEN,
        SUSPENDED.

    Returns:
        organization_id: Id for the newly created org
    """
    # make sure all required components present before attempting to add org
    if not all([name, phone, status]):
        return None

    new_organization = Organization(name=name, phone=phone, status=status)
    db.session.add(new_organization)
    db.session.commit()

    return new_organization.id


def org_registration(location, hours):
    """Create organization location and hours information in the database.

    This function registers an organization's location and its operating hours
    in the database, associating them with the current user’s organization.

    Parameters:
        location (dict): A dictionary containing the location details with keys
                    'street', 'zip-code', 'city', 'state', and 'neighborhood'.
        hours (dict): A dictionary containing the operating hours with keys
                      being days of the week and values being lists of opening
                      and closing time tuples.

    Returns:
        None
    """
    new_location = add_location(
        street_address=location["street"],
        zip_code=location["zip-code"],
        city=location["city"],
        state=location["state"],
        primary_location=True,
        neighborhood=location["neighborhood"],
    )

    # Associate location with organization
    assign_location_foreign_key_org_table(
        organization_id=current_user.organization.id,
        new_location_id=new_location.id,
    )

    for day in hours:
        for hours_segment in hours[day]:
            opening_time, closing_time = hours_segment
            new_hours = add_hours(
                day_of_week=day,
                opening_time=opening_time,
                closing_time=closing_time,
            )

            db.session.execute(
                insert(organizations_hours).values(
                    hours_id=new_hours.id,
                    organization_id=current_user.organization.id,
                )
            )

    db.session.commit()


def add_location(
    street_address, zip_code, city, state, primary_location, neighborhood
):
    """Add a new location to the database.

    This function creates a new location with the provided details and adds it
    to the database.

    Parameters:
        street_address (str): The street address of the location.
        zip_code (str): The zip code of the location.
        city (str): The city of the location.
        state (str): The state of the location.
        primary_location (bool): Indicates if this is the primary location.
        neighborhood (str): The neighborhood of the location.

    Returns:
        Location: The newly created Location object.
    """
    new_location = Location(
        street_address=street_address,
        zip_code=zip_code,
        city=city,
        state=state,
        primary_location=primary_location,
        neighborhood=neighborhood,
        created_by=current_user.id,
    )

    db.session.add(new_location)
    db.session.commit()

    return new_location


def add_hours(day_of_week, opening_time, closing_time):
    """Add new operating hours to the database.

    This function creates a new operating hours entry with the provided details
    and adds it to the database.

    Parameters:
        day_of_week (int): The day of the week ('Monday = 1, 'Tuesday' = 2, ..).
        opening_time (str): The opening time in HH:MM format.
        closing_time (str): The closing time in HH:MM format.

    Returns:
        Hours: The newly created Hours object.
    """
    new_hours = Hours(
        day_of_week=day_of_week,
        opening_time=opening_time,
        closing_time=closing_time,
        created_by=current_user.id,
    )

    db.session.add(new_hours)
    db.session.commit()

    return new_hours


def assign_location_foreign_key_org_table(organization_id, new_location_id):
    """Add location ID to organization table.

    This function updates the location ID of the specified organization.

    Parameters:
        organization_id (int): The ID of the organization to be updated.
        new_location_id (int): The ID of the new location to be assigned.

    Returns:
        None
    """
    organization_row = Organization.query.filter_by(id=organization_id).first()

    try:
        if not organization_row:
            raise ValueError(
                f"Organization id: {organization_id} isn't found in database"
            )
    except ValueError as e:
        print(e)

    organization_row.location_id = new_location_id
    db.session.commit()
    return


def change_organization_status(org_id):
    """Changes the status of an organization in the database.

    This function changes the status of an organization between 'VISIBLE' and
    'SUSPEND' in the database.

    Parameters:
        org_id (int): The ID of the org whose status needs to be toggled.

    Returns:
        Organization: The updated Organization object with the toggled status,
            or None if the organization is not found.
    """
    organization = Organization.query.get(org_id)

    if organization:
        # changes status to suspend if status is visible and vice-versa
        if organization.status == "ACTIVE":
            organization.status = "SUSPENDED"
        else:
            organization.status = "ACTIVE"

        db.session.commit()  # test on test db
        return organization
    else:
        return None


def extract_organization(organization_id):
    """Extracts detailed information about an organization.

    This function retrieves detailed information about an organization,
    including its primary location, operating hours, services, and languages
    spoken.

    Args:
        organization_id (int): The ID of the organization to be extracted.

    Returns:
        dict: A dictionary containing the organization's details such as name,
              phone, languages, services, hours, and primary location
              information.
    """
    org_info = Organization.query.filter_by(id=organization_id).first()
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
        # "email": user_info.email,
        "languages": language_list,
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


def retrieve_hours(all_hours):
    """Retrieves the operating hours for an organization.

    This function organizes the operating hours of an organization into a
    dictionary with days of the week as keys.

    Args:
        all_hours (list): A list of hours objects containing all hours.

    Returns:
        dict: A dictionary containing the operating hours for each
        day of the week.
    """
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


def extract_hour_info(current_hour, organization_hours, weekdays):
    """Extracts and organizes hour information for a specific day.

    Args:
        current_hour (object): An object containing the hour information
            for a specific day.
        organization_hours (dict): A dictionary to store the organized
             hour information.
        weekdays (dict): A dictionary mapping day numbers to day names.
    """
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
    """Retrieves all languages spoken at an organization.

    Args:
        org_reference (object): An object reference to the organization.

    Returns:
        list: A list of languages spoken at the organization.
    """
    all_languages = org_reference.languages
    language_list = []
    for curr_language in all_languages:
        language_list.append(curr_language.language)

    return language_list


def retrieve_services(all_services):
    """Retrieves detailed information about the services offered by an org.

    Args:
        all_services (list): A list of service objects provided by the
        organization.

    Returns:
        list: A list of dictionaries containing detailed information about
        each service.
    """
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
    """Retrieves all dates associated with a service.

    Args:
        all_dates (list): A list of date objects associated with a service.

    Returns:
        list: A list of dictionaries containing date information.
    """
    complete_date_info = []

    # Retrieve all dates for service
    for current_date in all_dates:
        complete_date_info.append(extract_date_info(current_date))

    return complete_date_info


def extract_date_info(current_date):
    """Extracts detailed information about a specific date.

    Args:
        current_date (object): An object containing date information.

    Returns:
        dict: A dictionary containing detailed information about the date.
    """
    single_date_info = {
        "date": current_date.date,
        "start_time": current_date.start_time,
        "end_time": current_date.end_time,
        "repeat": current_date.repeat,
    }
    return single_date_info


def retrieve_locations(all_locations):
    """Retrieves all location details associated with a service.

    Args:
        all_locations (list): A list of location objects associated with a
        service.

    Returns:
        list: A list of dictionaries containing location information.
    """
    complete_location_info = []

    # Retrieve all dates for service
    for current_location in all_locations:
        complete_location_info.append(extract_location_info(current_location))

    return complete_location_info


def extract_location_info(current_location):
    """Extracts detailed information about a specific location.

    Args:
        current_location (object): An object containing location information.

    Returns:
        dict: A dictionary containing detailed information about the location.
    """
    single_location_info = {
        "street address": current_location.street_address,
        "zip_code": current_location.zip_code,
        "city": current_location.city,
        "state": current_location.state,
        "primary_location": current_location.primary_location,
        "neighborhood" : current_location.neighborhood,
        }
    return single_location_info

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
    * create_organization_profile: Creates organization in the database.

Last updated:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/13/2024

Creation:
@Author: Madeleine Roberts @MadeleineKRoberts
@Date: 05/09/2024
"""

from new_arrivals_chi.app.database import db, User, Organization, Location, Hours, organizations_hours
from flask_login import current_user
from flask_bcrypt import Bcrypt
from sqlalchemy import insert
import ERROR

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
    """Creates org information in the database.

    Parameters:

    Returns:
        
    """
    new_location = add_location(
        street_address = location['street'],
        zip_code = location['zip-code'],
        city = location['city'],
        state = location['state'],
        primary_location = True,
        neighborhood = location['neighborhood']
    )

    # Associate location with organization
    assign_location_foreign_key_org_table(organization_id=current_user.organization.id, new_location_id=new_location.id)
    
    hours_ids = []
    for day in hours:
        for hours_segment in hours[day]:
            opening_time, closing_time = hours_segment
            new_hours = add_hours(
                day_of_week = day,
                opening_time = opening_time,
                closing_time = closing_time
            )

            db.session.execute(insert(organizations_hours).values(hours_id=new_hours.id, organization_id=current_user.organization.id))

    db.session.commit()

  

def add_location(street_address, zip_code, city, state, primary_location, neighborhood):
    new_location = Location(
        street_address = street_address,
        zip_code = zip_code,
        city = city,
        state = state,
        primary_location = primary_location,
        neighborhood = neighborhood,
        created_by = current_user.id

        #organization = db.relationship("Organization", back_populates="locations")
        #services = db.relationship("Service", secondary=location_services, back_populates="locations")
    )
    
    db.session.add(new_location)
    db.session.commit()

    return new_location

def add_hours(day_of_week, opening_time, closing_time):
    new_hours = Hours(
        day_of_week = day_of_week, 
        opening_time = opening_time, 
        closing_time = closing_time,
        created_by = current_user.id
    )
    
    db.session.add(new_hours)
    db.session.commit()

    return new_hours


def assign_location_foreign_key_org_table(organization_id, new_location_id):
     #organization_id = current_user.organization.id
     # new_location_id = new_location.id

    organization_row = Organization.query.filter_by(id=organization_id).first()

    try:
        if not organization_row:
            raise ERROR(f"Organization with id: {organization_id} cannot be found in database")
    except ERROR as e:
            print(e) 
    
    organization_row.location_id = new_location_id
    db.session.commit()
    return


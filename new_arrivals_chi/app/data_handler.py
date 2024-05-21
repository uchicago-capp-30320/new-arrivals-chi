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

from new_arrivals_chi.app.database import db, User, Organization
from flask_login import current_user
from flask_bcrypt import Bcrypt

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

def change_organization_status(org_id):
    """Changes the status of an organization in the database.

    This function changes the status of an organization between 'VISIBLE' and
    'SUSPEND' in the database.

    Parameters:
        org_id (int): The ID of the organization whose status needs to be toggled.

    Returns:
        Organization: The updated Organization object with the toggled status,
            or None if the organization is not found.
    """
    organization = Organization.query.get(org_id)

    if organization:
        # changes status to suspend if status is visible and vice-versa
        if organization.status == 'ACTIVE':
            organization.status = 'SUSPENDED'
        else:
            organization.status = 'ACTIVE'

        db.session.commit()
        return organization
    else:
        return None

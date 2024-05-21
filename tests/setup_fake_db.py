"""Project: New Arrivals Chicago.

File name: setup_fake_db.py
Associated Files: main.py, database.py, db_test.py

This script initializes a Flask application and uses it to generate
fake data for testing purposes.

Methods:
    * main — Sets up logging, initializes the Flask application,
    creates the database, and generates fake data.

Last updated:
@Author: Aaron Haefner @aaronhaefner
@Date: 2024-05-07

Creation:
@Author: Aaron Haefner @aaronhaefner
@Date: 2024-05-07
"""

import os
from new_arrivals_chi.app.main import create_app, db
from new_arrivals_chi.app.utils import setup_logger
from sqlalchemy.orm import Session
from tests.utils import (
    create_fake_user,
    create_fake_organization,
    create_fake_location,
    create_fake_hours,
    create_fake_language,
    create_fake_service,
    create_fake_service_date,
)
from new_arrivals_chi.app.database import organizations_hours


def add_user(session):
    """Create and add a fake user to the session."""
    user = create_fake_user(setup_logger)
    session.add(user)
    session.flush()
    return user


def add_organization(session, user):
    """Create and add a fake organization associated with the user."""
    organization = create_fake_organization(user)
    session.add(organization)
    session.flush()
    return organization


def add_location(session, user):
    """Create and add a fake location associated with the user."""
    location = create_fake_location(user.id)
    session.add(location)
    session.flush()
    return location


def add_hours(session, user):
    """Create and add fake hours associated with the user."""
    hours = create_fake_hours(user.id)
    session.add(hours)
    session.flush()
    return hours


def add_language(session, organization, user):
    """Create and add a fake language associated with the organization."""
    language = create_fake_language()
    language.created_by = user.id
    organization.languages.append(language)
    session.add(language)


def add_service(session, organization, user):
    """Create and add a fake service associated with the organization."""
    service = create_fake_service(user.id)
    service.created_by = user.id
    organization.services.append(service)
    session.add(service)
    return service


def add_service_date(session, service, user):
    """Create and add a fake service date associated with the service."""
    service_date = create_fake_service_date(user.id)
    service.service_dates.append(service_date)
    session.add(service_date)


def add_service_location(session, service, user):
    """Create and add a fake location associated with the service."""
    service_location = create_fake_location(user.id)
    service.locations.append(service_location)
    session.add(service_location)


def populate_database(
    session: Session,
    num_organizations=10,
    num_services=3,
    num_service_dates=2,
    num_service_locations=2,
    logger=setup_logger,
):
    """Populate the database with fake data.

    Parameters:
        session (Session): The SQLAlchemy session object.
        num_organizations (int): Number of organizations to create.
        num_services (int): Number of services to create per organization.
        num_service_dates (int): Number of service dates to create per service.
        num_service_locations (int): Number of locations to create per service.
        logger (Logger, optional): Logger for recording operations.

    Returns:
        None; logs data creation process and outcomes.
    """
    logger = setup_logger("populate_database")
    logger.info("Starting to create fake data")
    try:
        for _ in range(num_organizations):
            user = add_user(session)
            organization = add_organization(session, user)
            user.organization_id = organization.id
            session.add(user)

            location = add_location(session, user)
            hours = add_hours(session, user)

            organization.location_id = location.id
            organization.hours_id = hours.id
            session.add(organization)

            # Populate organizations_hours table
            session.execute(
                organizations_hours.insert().values(
                    organization_id=organization.id, hours_id=hours.id
                )
            )
            add_language(session, organization, user)

            # Add services
            for _ in range(num_services):
                service = add_service(session, organization, user)

                for _ in range(num_service_dates):
                    add_service_date(session, service, user)

                for _ in range(num_service_locations):
                    add_service_location(session, service, user)

        session.commit()
        logger.info("Fake data creation completed successfully")
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating data: {e}, rolling back changes")
        raise


def main():
    """Main function to initialize fake database.

    Uses the populate_database function to
    generate fake data for testing purposes.

    Returns:
        None; logs the completion of fake data generation.
    """
    if os.path.exists("./instance/test_fake_data.db"):
        os.remove("./instance/test_fake_data.db")
    logger = setup_logger("populate_database")
    logger.info("Starting the application setup for fake data creation.")

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///./test_fake_data.db",
        }
    )

    with app.app_context():
        db.create_all()

        num_organizations = 10
        populate_database(db.session, num_organizations, logger=logger)

        logger.info("Fake data has been created successfully.")

        return app, db


if __name__ == "__main__":
    main()

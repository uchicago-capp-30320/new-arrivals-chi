"""Project: New Arrivals Chicago.

File name: setup_fake_db.py
Associated Files: main.py, database.py

This script initializes a Flask application and uses it to generate
fake data for testing purposes.

Methods:
    * main — Sets up logging, initializes the Flask application,
    creates the database, and generates fake data.
"""

import os
import random
from faker import Faker
from new_arrivals_chi.app.main import create_app, db
from new_arrivals_chi.app.database import (
    User,
    Organization,
    Location,
    Hours,
    Language,
    Service,
    ServiceDate,
    organizations_hours,
)
from new_arrivals_chi.app.utils import setup_logger
from tests.constants import (
    OPENING_TIMES,
    CLOSING_TIMES,
    SERVICE_CATEGORIES,
    SERVICES,
    ACCESS_TYPES,
    SERVICE_NOTES,
    FAKE_NEIGHBORHOODS,
)
from sqlalchemy.orm import Session

fake = Faker()


def create_fake_user():
    """Create a single fake user instance.

    Returns:
        A User instance with a randomly generated email and role.
    """
    return User(
        email=fake.email(),
        role=fake.random_element(elements=("admin", "standard")),
        password=fake.password(),
    )


def create_fake_organization(user):
    """Create a single fake organization instance.

    Parameters:
        user (User): The user who created the organization.

    Returns:
        An Organization instance with randomly generated name and phone number.
    """
    return Organization(
        name=fake.company(),
        phone=fake.phone_number(),
        image_path=fake.image_url(),
        status=fake.random_element(elements=("ACTIVE", "SUSPENDED", "HIDDEN")),
        created_by=user.id,
        updated_by=user.id,
    )


def create_fake_hours(user_id):
    """Create a single fake hours instance with realistic business hours.

    Parameters:
        user_id (int): The ID of the user who created the hours.

    Returns:
        An Hours instance with randomly generated realistic business hours.
    """
    return Hours(
        day_of_week=fake.random_int(min=0, max=6),
        opening_time=random.choice(OPENING_TIMES),
        closing_time=random.choice(CLOSING_TIMES),
        created_by=user_id,
        created_at=fake.date_time_this_decade(),
    )


def create_fake_language():
    """Create a valid language instance (e.g., 'en' or 'es', or 'fake').

    Returns:
        A Language instance with a predefined valid language.
    """
    languages = ["en", "es", "fake"]
    return Language(
        language=fake.random_element(elements=languages),
        created_at=fake.date_time_this_decade(),
    )


def create_fake_service(user_id):
    """Create a single fake service instance.

    Parameters:
        user_id (int): The ID of the user who created the service.

    Returns:
        A Service instance with randomly selected standardized data.
    """
    return Service(
        category=random.choice(SERVICE_CATEGORIES),
        service=random.choice(SERVICES),
        access=random.choice(ACCESS_TYPES),
        service_note=random.choice(SERVICE_NOTES),
        created_at=fake.date_time_this_decade().replace(microsecond=0),
        created_by=user_id,
    )


def create_fake_service_date(user_id):
    """Create a single fake service date instance.

    Parameters:
        user_id (int): The ID of the user who created the service date.

    Returns:
        ServiceDate instance with random date, start and end times, and repeat.
    """
    return ServiceDate(
        date=fake.date_this_decade(),
        start_time=random.choice(OPENING_TIMES),
        end_time=random.choice(CLOSING_TIMES),
        repeat=fake.random_element(
            elements=[
                "every day",
                "every week",
                "every month",
                "every other week",
            ]
        ),
        created_at=fake.date_time_this_decade(),
        created_by=user_id,
    )


def create_fake_location(user_id):
    """Create a single fake location instance that requires a user.

    Parameters:
        user_id (int): The ID of the user who created the location.

    Returns:
        A Location instance with randomly generated address and state info.
    """
    return Location(
        street_address=fake.street_address(),
        zip_code=fake.zipcode(),
        city=fake.city(),
        state=fake.state(),
        primary_location=fake.boolean(),
        created_by=user_id,
        neighborhood=fake.random_element(elements=FAKE_NEIGHBORHOODS),
        created_at=fake.date_time_this_decade(),
    )


def add_user(session):
    """Create and add a fake user to the session."""
    user = create_fake_user()
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

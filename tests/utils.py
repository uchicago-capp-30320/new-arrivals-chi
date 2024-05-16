"""Project: New Arrivals Chicago.

File name: db_test.py
Associated Files: database.py, models.py

This script is used for generating fake data for testing the database models
and relationships within the New Arrivals Chicago Flask application.

Methods:
    * create_fake_location — Create a fake location requiring a user ID.
    * create_fake_hours — Create a fake hours.
    * create_fake_organization — Create a fake organization.
    * create_fake_user — Create a fake user associated with an organization.
    * create_fake_data — Generate fake data for testing multiple users.
    * get_record_by_id — Retrieve a single record by its ID.
    * get_record_by_attribute — Retrieve a single record by specified attribute.
    * fetch_data — Fetch and print data from the database to verify insertion.
    * test_user_organization_creation — Create and retrieve users and orgs.

Last updated:
@Author: Aaron Haefner @aaronhaefner
@Date: 2024-05-16

Creation:
@Author: Aaron Haefner @aaronhaefner
@Date: 2024-05-16
"""

import random
from faker import Faker
from new_arrivals_chi.app.database import (
    User,
    Organization,
    Location,
    Hours,
    Language,
    Service,
    ServiceDate,
)
from tests.constants import (
    OPENING_TIMES,
    CLOSING_TIMES,
    SERVICE_CATEGORIES,
    SERVICES,
    ACCESS_TYPES,
    SERVICE_NOTES,
    FAKE_NEIGHBORHOODS,
)

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

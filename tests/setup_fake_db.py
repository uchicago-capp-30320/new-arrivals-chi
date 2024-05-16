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


def populate_database(session: Session, num_organizations=10, logger=None):
    """Populate the database with fake data.

    Parameters:
        session (Session): The SQLAlchemy session object.
        num_organizations (int): Number of organizations to create.
        logger (Logger, optional): Logger for recording operations.

    Returns:
        None; logs data creation process and outcomes.
    """
    logger.info("Starting to create fake data") if logger else None
    try:
        for _ in range(num_organizations):
            # Create and add initial user without committing
            user = create_fake_user()
            session.add(user)
            session.flush()  # Flush to get the user ID without committing

            # Create and add organization with user ID for created_by and updated_by
            organization = create_fake_organization(user)
            session.add(organization)
            session.flush()  # Flush to get the organization ID without committing

            # Backfill user with organization_id
            user.organization_id = organization.id
            session.add(user)

            # Create and add location associated with the user
            location = create_fake_location(user.id)
            session.add(location)
            session.flush()  # Flush to get the location ID without committing

            # Create and add hours associated with the user
            hours = create_fake_hours(user.id)
            session.add(hours)
            session.flush()  # Flush to get the hours ID without committing

            # Update organization with location_id and hours_id
            organization.location_id = location.id
            organization.hours_id = hours.id

            session.add(organization)

            # Populate organizations_hours table
            session.execute(organizations_hours.insert().values(
                organization_id=organization.id,
                hours_id=hours.id
            ))

            # Create and add languages associated with the organization
            for _ in range(3):
                language = create_fake_language()
                language.created_by = user.id
                organization.languages.append(language)
                session.add(language)

            # Create and add services associated with the organization
            for _ in range(3):
                service = create_fake_service(user.id)
                service.created_by = user.id
                organization.services.append(service)
                session.add(service)

                # Create and add service dates associated with the service
                for _ in range(2):
                    service_date = create_fake_service_date(user.id)
                    service.service_dates.append(service_date)
                    session.add(service_date)

                # Create and add locations associated with the service
                for _ in range(2):
                    service_location = create_fake_location(user.id)
                    service.locations.append(service_location)
                    session.add(service_location)

        session.commit()
        logger.info("Fake data creation completed successfully") if logger else None
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating data: {e}, rolling back changes") if logger else None
        raise


def main():
    """Main function to initialize fake database.

    Uses the populate_database function to
    generate fake data for testing purposes.

    Returns:
        None; logs the completion of fake data generation.
    """
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
        populate_database(db.session, num_organizations, logger)

        logger.info("Fake data has been created successfully.")

        return app, db


if __name__ == "__main__":
    main()

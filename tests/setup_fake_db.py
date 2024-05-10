"""Project: New Arrivals Chicago.

File name: create_fake_data.py
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
from db_test import create_fake_data


def main():
    """Main function to initialize fake database.

    Uses the create_fake_data function from db_test to
    generate fake data for testing purposes.

    Returns:
        None; logs the completion of fake data generation.
    """
    logger = setup_logger("FakeDataCreator")
    logger.info("Starting the application setup for fake data creation.")

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///./test_fake_data.db",
        }
    )

    with app.app_context():
        db.create_all()

        num_users = 10
        create_fake_data(num_users, db, logger)

        logger.info("Fake data has been created successfully.")

        return app, db


if __name__ == "__main__":
    main()

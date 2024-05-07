import logging
from flask import Flask
from new_arrivals_chi.app.main import create_app, db
from new_arrivals_chi.app.database import User, Organization, Location, Hours
from db_test import create_fake_data

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('FakeDataCreator')

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///./test_fake_data.db',  # Ensure this points to a test DB
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    # Run within the application context
    with app.app_context():
        db.create_all()

        num_users = 10
        create_fake_data(num_users, db, logger)

        logger.info("Fake data has been created successfully.")

if __name__ == '__main__':
    main()

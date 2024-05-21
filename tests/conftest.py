"""Project: New Arrivals Chi.

File name: conftest.py

Associated Files:
   This script defines various pytest fixtures used across the test suite for
   the New Arrivals Chi application.

Fixtures:
   - app: Flask application instance configured for testing.
   - client: A test client for the app.
   - database: Sets up a clean database before each test, tears down after.
   - setup_logger: Creates a logger with file and console handlers for testing.
   - capture_templates: Captures the templates rendered during a test.
   - test_user: Creates a test user in the database before test, removes after.
   - login_client: Logs in user for testing routes that require authentication.

Last updated:
@Author: Madeleine Roberts @madeleinekroberts
@Date: 2024-05-09

Creation:
@Author: Aaron Haefner @aaronhaefner
@Date: 2024-05-06
"""

import pytest
import logging
import os
from datetime import datetime, timedelta
from new_arrivals_chi.app.main import create_app, db, User
from new_arrivals_chi.app.database import Organization
from flask import template_rendered
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


@pytest.fixture(scope="module")
def app():
    """Provides the Flask application instance configured for testing.

    Returns:
        Yields the Flask application instance with test configurations applied.
    """
    test_config = {
        "SERVER_NAME": "localhost.localdomain:5000",
        "APPLICATION_ROOT": "/",
        "PREFERRED_URL_SCHEME": "http",
        "TESTING": True,
        "DEBUG": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test_fake_data.db",
        "SECRET_KEY": "testing_key",
        "PERMANENT_SESSION_LIFETIME": timedelta(hours=12),
    }
    app = create_app(config_override=test_config)
    with app.app_context():
        # db.create_all()
        yield app
        # db.session.remove()
        # db.drop_all()


@pytest.fixture(scope="module")
def client(app):
    """Provides a test client for the app.

    Parameters:
        app (Flask): The Flask app instance for which to create a test client.

    Returns:
        The test client for the given Flask app.
    """
    return app.test_client()


@pytest.fixture(scope="function")
def query_test_user(app):
    """Fixture to query an existing test user from the database."""
    with app.app_context():
        user = User.query.get(1)
        if user is None:
            raise ValueError("Test user with id=1 not found in the database.")
        yield user


@pytest.fixture(scope="function")
def database(app):
    """Sets up a clean database before each test and tears it down after.

    Parameters:
        app (Flask): The Flask app instance to use for test database setup.

    Returns:
        Yields the database instance to be used in tests.
    """
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def setup_logger():
    """Creates a logger with file and console handlers.

    Returns:
        A function that creates and returns a configured logger.
    """

    def create_logger(name: str, level=logging.INFO) -> logging.Logger:
        log_directory = "logs"
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"{name}_{timestamp}.log"
        log_path = os.path.join(log_directory, log_filename)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    return create_logger


# Reference: https://stackoverflow.com/questions/57006104/
@pytest.fixture(scope="function")
def capture_templates(app):
    """Create a function to retrieve the templates rendered."""
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


@pytest.fixture(scope="function")
def test_organization(client):
    """Create a test user in the database before each test and remove after."""
    org_test_case = Organization(
        name="Test Org", phone="123-456-7891", status="ACTIVE"
    )
    db.session.add(org_test_case)
    db.session.commit()

    yield org_test_case

    db.session.delete(org_test_case)
    db.session.commit()


@pytest.fixture(scope="function")
def test_user(client, test_organization):
    """Create test user with associated org in db before test, remove after."""
    user_password = bcrypt.generate_password_hash("TestP@ssword!").decode(
        "utf-8"
    )
    user_test_case = User(
        email="test@example.com",
        password=user_password,
        organization_id=test_organization.id,
    )
    db.session.add(user_test_case)
    db.session.commit()

    yield user_test_case

    db.session.delete(user_test_case)
    db.session.commit()


@pytest.fixture(scope="function")
def logged_in_state(client, test_user):
    """Logs in a user for testing routes that require authentication."""
    client.post(
        "/login",
        data={"email": "test@example.com", "password": "TestP@ssword!"},
        follow_redirects=True,
    )
    yield client

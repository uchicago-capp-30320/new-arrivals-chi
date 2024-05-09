"""
Project: New Arrivals Chi
File name: conftest.py
Associated Files:

This script ...

Methods:


Last updated:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 2024-05-07

Creation:
@Author: Aaron Haefner @aaronhaefner
@Date: 2024-05-06
"""

import pytest
import logging
import os
from datetime import datetime
from werkzeug.security import generate_password_hash
from new_arrivals_chi.app.main import create_app, db, User
from flask import template_rendered


@pytest.fixture(scope="module")
def app():
    """Provides the Flask application instance configured for testing."""
    test_config = {
        "SERVER_NAME": "localhost.localdomain:5000",
        "APPLICATION_ROOT": "/",
        "PREFERRED_URL_SCHEME": "http",
        "TESTING": True,
        "DEBUG": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "testing_key",
    }
    app = create_app(config_override=test_config)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="module")
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope="function")
def database(app):
    """
    Set up a clean database before each test and tear it down after.
    """
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def setup_logger():
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


# Reference: https://stackoverflow.com/questions/57006104/how-to-test-flask-view-context-and-templates-using-pytest
@pytest.fixture(scope="function")
def capture_templates(app):
    """
    Create a function to retrieve the templates rendered.
    """
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


@pytest.fixture(scope="function")
def test_user(client):
    """
    Create a test user in the database before each test and remove it after.
    """
    user_password = generate_password_hash(
        "TestP@ssword!", method="pbkdf2:sha256"
    )
    test_user = User(email="test@example.com", password=user_password)
    db.session.add(test_user)
    db.session.commit()

    yield test_user

    db.session.delete(test_user)
    db.session.commit()


@pytest.fixture(scope="function")
def login_client(client):
    """
    Logs in a user for testing routes that require authentication.
    """
    client.post(
        "/login",
        data={"email": "test@example.com", "password": "TestP@ssword!"},
        follow_redirects=True,
    )
    yield client

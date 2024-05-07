"""Project: New Arrivals Chicago.

File name: conftest.py
Associated Files: main.py, models.py, tests/.

Provides pytest fixtures for creating a Flask application context,
a client for testing, and a database setup for function-scoped tests.

Methods:
    * app — Provides a configured Flask application for testing.
    * client — Provides a test client for the application.
    * database — Sets up and tears down a clean database for each test.
    * setup_logger — Creates a logger with a file and console handler.

Last updated:
@Author: Aaron Haefner @aaronhaefner
@Date: 2024-05-07

Creation:
@Author: Aaron Haefner @aaronhaefner
@Date: 2024-04-23
"""

import pytest
import logging
import os
from datetime import datetime
from new_arrivals_chi.app.main import create_app, db


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
    }
    app = create_app(config_override=test_config)
    with app.app_context():
        yield app


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

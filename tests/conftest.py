import pytest
import logging
import os
from datetime import datetime
from new_arrivals_chi.app.main import create_app, db


@pytest.fixture(scope="module")
def app():
    """Provides the Flask application instance configured for testing."""
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

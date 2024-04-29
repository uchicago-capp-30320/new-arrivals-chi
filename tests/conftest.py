import os
import pytest
from new_arrivals_chi.app.main import app as flask_app


@pytest.fixture(scope="module")
def app():
    """Provides the Flask application instance configured for testing."""
    flask_app.config["TESTING"] = True
    flask_app.config["DEBUG"] = False
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    flask_app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    yield flask_app  # Yield the flask_app instance for use in tests


@pytest.fixture(scope="module")
def client(app):
    """A test client for the app."""
    return app.test_client()

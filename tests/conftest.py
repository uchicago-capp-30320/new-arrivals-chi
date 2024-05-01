import pytest

from new_arrivals_chi.app.main import app as flask_app


@pytest.fixture(scope="module")
def app():
    """Provides the Flask application instance configured for testing."""
    flask_app.config[
        "SERVER_NAME"
    ] = "localhost.localdomain:5000"  # Example server name
    flask_app.config["APPLICATION_ROOT"] = "/"  # Default root
    flask_app.config["PREFERRED_URL_SCHEME"] = "http"

    with flask_app.app_context():  # Pushes an application context
        yield flask_app


@pytest.fixture(scope="module")
def client(app):
    """A test client for the app."""
    return app.test_client()

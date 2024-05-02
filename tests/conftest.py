import pytest

from new_arrivals_chi.app.main import create_app


@pytest.fixture(scope="module")
def app():
    """Provides the Flask application instance configured for testing."""
    app = create_app()
    app.config[
        "SERVER_NAME"
    ] = "localhost.localdomain:5000"  # Example server name
    app.config["APPLICATION_ROOT"] = "/"  # Default root
    app.config["PREFERRED_URL_SCHEME"] = "http"
    app.config["TESTING"] = True
    app.config["DEBUG"] = False

    with app.app_context():  # Pushes an application context
        yield app


@pytest.fixture(scope="module")
def client(app):
    """A test client for the app."""
    return app.test_client()

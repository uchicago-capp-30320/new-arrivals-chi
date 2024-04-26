# conftest.py
import pytest
from new_arrivals_chi.app.main import app

@pytest.fixture(scope='module')
def app():
    """Provides an instance of the main Flask application configured for testing."""
    app.config['TESTING'] = True
    app.config['DEBUG'] = False  # Ensure debug is off for testing
    return app

@pytest.fixture(scope='module')
def client(app):
    """Provides a test client from the Flask application."""
    return app.test_client()

import pytest
from new_arrivals_chi.app.main import app
from bs4 import BeautifulSoup


@pytest.fixture
def client():
    """Configure the Flask test client for testing."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_page_status(client):
    """Ensure the home page returns a 200 status code."""
    response = client.get("/")
    assert response.status_code == 200


def test_home_contains_welcome_message(client):
    """Check if the home page contains the welcome message."""
    response = client.get("/")
    html_content = response.data.decode("utf-8")
    assert "Welcome" in html_content


def test_home_has_navigation_bar(client):
    """Verify that the navigation bar contains all required links."""
    response = client.get("/")
    html_content = response.data.decode("utf-8")
    assert "<nav" in html_content
    assert "Home" in html_content
    assert "Profile" in html_content
    assert "Legal" in html_content
    assert "Login" in html_content
    assert "Sign Up" in html_content


def test_home_language_setting(client):
    """Ensure the home page supports Spanish language settings."""
    response = client.get("/?lang=es")
    html_content = response.data.decode("utf-8")
    assert "Bienvenido" in html_content


def test_home_page_language_content(client):
    """Check language-specific content rendering on the home page."""

    response = client.get("/")
    html_content = response.data.decode("utf-8")
    assert "Welcome" in html_content
    assert (
        "Find essential support for legal, health, and food needs."
        in html_content
    )
    assert "Please click below to begin:" in html_content

    response = client.get("/?lang=es")
    html_content = response.data.decode("utf-8")
    assert "Bienvenido" in html_content
    assert (
        "Encuentra apoyo para tus necesidades legales, de salud o de comida."
        in html_content
    )
    assert "Por favor haz click abajo para comenzar:" in html_content


def test_home_page_buttons(client):
    """Verify that all necessary buttons are present on the home page."""
    response = client.get("/")
    html_content = response.data.decode("utf-8")
    soup = BeautifulSoup(html_content, "html.parser")

    legal_button = soup.find("button", string="Legal")
    health_button = soup.find("button", string="Health")

    assert legal_button is not None
    assert health_button is not None


def test_home_page_button_links(client):
    """Test that buttons on the home page link correctly in English/Spanish."""
    # Test button actions in English
    response = client.get("/")
    html_content = response.data.decode("utf-8")
    assert "navigateTo('/legal', 'en')" in html_content
    assert "window.location.href='/health'" in html_content
    assert "window.location.href='/food'" in html_content

    # Test button actions in Spanish
    response = client.get("/?lang=es")
    html_content = response.data.decode("utf-8")
    assert "navigateTo('/legal', 'es')" in html_content
    assert "window.location.href='/health'" in html_content
    assert "window.location.href='/food'" in html_content

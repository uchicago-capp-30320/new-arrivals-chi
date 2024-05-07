"""Project: New Arrivals Chicago.

File name: test_home_page.py
Associated Files: main.py, views.py, templates/home.html.

Tests for the home page of the New Arrivals Chicago Flask application.

Methods:
    * test_home_page_status — Ensure the home page returns 200 status code.
    * test_home_contains_welcome_message — Check home page welcome message.
    * test_home_language_setting — Ensure home page supports Spanish language.
    * test_home_page_buttons — Verify buttons are present on home page.
    * test_home_page_button_links — Test that buttons link correctly.

Last updated:
@Author: Aaron Haefner @aaronhaefner
@Date: 2024-05-07

Creation:
@Author: Aaron Haefner @aaronhaefner
@Date: 2024-04-30
"""

from flask import url_for


def test_home_page_status(client):
    """Ensure the home page returns 200 status code.

    Parameters:
        client (FlaskClient): The test client for making requests.

    Returns:
        Asserts that the response status code is 200.
    """
    response = client.get(url_for("main.home"))
    assert response.status_code == 200


def test_home_contains_welcome_message(client):
    """Check if the home page contains welcome message.

    Parameters:
        client (FlaskClient): The test client for making requests.

    Returns:
        Asserts that "Welcome" is in the response data.
    """
    response = client.get(url_for("main.home"))
    assert "Welcome" in response.data.decode("utf-8")


def test_home_language_setting(client):
    """Ensure the home page supports Spanish language settings.

    Parameters:
        client (FlaskClient): The test client for making requests.

    Returns:
        Asserts that "Bienvenido" is in response data when requested in Spanish.
    """
    response = client.get(url_for("main.home", lang="es"))
    assert "Bienvenido" in response.data.decode("utf-8")


def test_home_page_buttons(client):
    """Verify that all necessary buttons are present on the home page.

    Parameters:
        client (FlaskClient): The test client for making requests.

    Returns:
        Asserts that buttons are present in the response data.
    """
    response = client.get(url_for("main.home"))
    html_content = response.data.decode("utf-8")
    assert "Legal" in html_content
    assert "Health" in html_content
    assert "Food" in html_content


def test_home_page_button_links(client):
    """Test that buttons link correctly in both English and Spanish.

    Parameters:
        client (FlaskClient): The test client for making requests.

    Returns:
        Asserts that button navigation links are correct
        for both English and Spanish language settings.
    """
    # Test English links
    response = client.get(url_for("main.home"))
    html_content = response.data.decode("utf-8")
    assert "navigateTo('/legal', 'en')" in html_content
    assert "navigateTo('/health', 'en')" in html_content
    assert "window.location.href='/food'" in html_content

    # Test Spanish links
    response = client.get(url_for("main.home", lang="es"))
    html_content = response.data.decode("utf-8")
    assert "navigateTo('/legal', 'es')" in html_content
    assert "navigateTo('/health', 'es')" in html_content
    assert "window.location.href='/food'" in html_content

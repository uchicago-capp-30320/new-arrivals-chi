# test_home_page.py
import pytest
from flask import url_for

def test_home_page_status(client):
    """Ensure the home page returns a 200 status code."""
    response = client.get(url_for('main.home'))
    assert response.status_code == 200

def test_home_contains_welcome_message(client):
    """Check if the home page contains the welcome message."""
    response = client.get(url_for('main.home'))
    assert 'Welcome' in response.data.decode('utf-8')

def test_home_language_setting(client):
    """Ensure the home page supports Spanish language settings."""
    response = client.get(url_for('main.home', lang='es'))
    assert 'Bienvenido' in response.data.decode('utf-8')

def test_home_page_buttons(client):
    """Verify that all necessary buttons are present on the home page."""
    response = client.get(url_for('main.home'))
    html_content = response.data.decode('utf-8')
    assert 'Legal' in html_content
    assert 'Health' in html_content
    assert 'Food' in html_content

def test_home_page_button_links(client):
    """Test that buttons on the home page link correctly in both English and Spanish."""
    # Test English links
    response = client.get(url_for('main.home'))
    html_content = response.data.decode('utf-8')
    assert "navigateTo('/legal', 'en')" in html_content
    assert "window.location.href='/health'" in html_content
    assert "window.location.href='/food'" in html_content

    # Test Spanish links
    response = client.get(url_for('main.home', lang='es'))
    html_content = response.data.decode('utf-8')
    assert "navigateTo('/legal', 'es')" in html_content
    assert "window.location.href='/health'" in html_content
    assert "window.location.href='/food'" in html_content

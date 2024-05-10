import pytest
from flask import session
from werkzeug.datastructures import MultiDict
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from bs4 import BeautifulSoup


def get_csrf_token_from_response(html):
    """
    Parses CSRF token from HTML response.
    """
    soup = BeautifulSoup(html, 'html.parser')
    token = soup.find('input', {'name': 'csrf_token'})['value']
    return token

def test_login_form_rejection_without_csrf(client):
    """
    Ensure the login form rejects a submission without a CSRF token.
    """
    response = client.post('/login', data={
        'email': 'user@example.com',
        'password': 'securepassword'
    }, follow_redirects=True)
    assert 'The CSRF token is missing.' in response.data.decode() or response.status_code == 400, "Form should reject submission without CSRF token"


def test_login_form_acceptance_with_csrf(client, app):
    """
    Ensure the login form accepts a submission with a valid CSRF token.
    """
    # Get the login page to retrieve the CSRF token
    response = client.get('/login')
    csrf_token = get_csrf_token_from_response(response.data.decode())

    # Submit the form with CSRF token
    response = client.post('/login', data={
        'email': 'user@example.com',
        'password': 'Str0ngP@$$word123!C0ntre$namUyfue&t3',
        'csrf_token': csrf_token
    }, follow_redirects=True)
    assert response.status_code == 200, "Form should accept submission with valid CSRF token"

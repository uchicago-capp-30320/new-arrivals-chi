import pytest
from flask import session
from werkzeug.datastructures import MultiDict
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from bs4 import BeautifulSoup
from flask_wtf.csrf import CSRFProtect, generate_csrf

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


#### new function to test
# @authorize.route("/login", methods=["POST"])
# def login_post():
#     """Processes the login request.

#     Returns:
#         Redirects to the user's profile page if login is successful,
#         otherwise redirects back to the login page with a flash message.
#     """
#     if request.form.get("csrf_token") != session.get("csrf_token"):
#         flash("Invalid CSRF token. Please try again.")
#         return redirect(url_for("authorize.login"))
#     email = request.form.get("email").lower()
#     password = request.form.get("password")
#     remember = True if request.form.get("remember") else False

#     user = User.query.filter_by(email=email).first()

#     # check if the user actually exists & password is correct
#     if not user or not verify_password(user.password, password):
#         flash("Please check your login details and try again.")
#         return redirect(
#             url_for("authorize.login")
#         )  # if the user doesn't exist or password is wrong, reload the page

#     # if the above check passes, then we know the user has the right credentials
#     login_user(user, remember=remember)
#     return redirect(url_for("main.profile"))

def test_login_post_invalid_csrf(client):
    """
    Ensure the login form rejects a submission with an invalid CSRF token.
    """
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'TestP@ssword!4234m!@3',
        'csrf_token': 'invalid_csrf_token'
    }, follow_redirects=True)
    assert 'Invalid CSRF token. Please try again.' in response.data.decode() or response.status_code == 400, "Form should reject submission with invalid CSRF token"

def test_login_post_valid_csrf(client, test_user):
    """
    Ensure the login form accepts a submission with a valid CSRF token.
    """
    response = client.get('/login')
    csrf_token = get_csrf_token_from_response(response.data.decode())

    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'TestP@ss3fsadf3!@!@#',
        'csrf_token': csrf_token
    }, follow_redirects=True)
    assert response.status_code == 200, "Form should accept submission with valid CSRF token"

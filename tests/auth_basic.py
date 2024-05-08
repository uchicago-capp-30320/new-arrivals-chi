"""
Project: New Arrivals Chi
File name: auth_basic.py
Associated Files:
    new_arrivals_chi/app/main.py,
    new_arrivals_chi/app/database.py,
    templates: signup.html, login.html, home.html, profile.html

This test suite performs basic validation of the user authorization routes 
including signup, login, and logout functionalities for the New Arrivals 
Chicago portal.

Methods:
    * create_app — Sets up the Flask application for testing.
    * setUp — Prepares the database and a test user before each test.
    * tearDown — Cleans up the database after each test.
    * test_signup_route — Tests the accessibility of the signup route.
    * test_signup_post_invalid_email — Tests signup with an invalid email.
    * test_signup_post_invalid_password — Tests signup with an invalid password.
    * test_signup_post_valid_credentials — Tests signup with valid credentials.
    * test_signup_post_weak_password — Tests signup with a weak password.
    * test_login_route — Tests the accessibility of the login route.
    * test_login_valid_credentials — Tests login with valid credentials.
    * test_login_invalid_credentials — Tests login with invalid credentials.
    * test_logout — Tests the logout functionality.
    * test_logout_not_logged_in — Tests the logout route when no user logged in.

Last updated:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/06/2024

Creation:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/06/2024
"""

import pytest
from flask import url_for
from flask import template_rendered
from new_arrivals_chi.app.main import create_app, db
from new_arrivals_chi.app.database import User
from werkzeug.security import generate_password_hash


def test_signup_route(client):
    """
    Tests the accessibility of the signup route by making a GET request 
    and verifying the response.

    Returns:
        Asserts that the response status code is 200 and that the correct 
        template 'signup.html' is used.
    """
    with capture_templates() as templates:
        response = client.get("/signup")
        assert response.status_code == 200
        assert b"Sign Up" in response.data  
        assert len(templates) == 1
        assert templates[0][0].name == 'signup.html'


def test_signup_post_invalid_email(client):
    """
    Tests the signup functionality with an invalid email format. Verifies 
    that the system correctly identifies the email as invalid and returns 
    to the signup page.

    Returns:
        Asserts that the response status code is 200, the correct template 
        'signup.html' is used, and an appropriate error message is included 
        in the response.
    """
    response = client.post(
        "/signup",
        data={
            "email": "bad_email",  # invalid email format
            "password": "TestP@ssword!",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Please enter a valid email address" in response.data

def test_signup_post_invalid_password(client):
    """
    Tests the signup functionality with an invalid password. Ensures that 
    the application rejects passwords that do not meet the specified 
    security criteria.

    Returns:
        Asserts that the response status code is 200, the 'signup.html' 
        template is used, and an appropriate error message is displayed.
    """
    response = client.client.post(
        "/signup",
        data={
            "email": "test@example.com",  # invalid password
            "password": "password!",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Please enter a valid password" in response.data

def test_signup_post_valid_credentials(client):
    """
    Tests the signup functionality with valid email and password. 
    This test verifies if the application correctly handles valid 
    registration credentials and redirects to the home page.

    Returns:
        Asserts that the response status code is 200, the 'home.html' 
        template is used after successful signup.
    """
    response = client.client.post(
        "/signup",
        data={
            "email": "new_user@example.com",  # valid email format
            "password": "StrongPassword123!",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    client.assert_template_used("home.html")

def test_signup_post_weak_password(client):
    """
    Tests the signup functionality with a weak password to verify that the 
    system enforces strong password requirements.

    Returns:
        Asserts that the response status code is 200, the 'signup.html' 
        template is reused, and an error message regarding password strength 
        is displayed.
    """
    response = client.client.post(
        "/signup",
        data={"email": "new_user@example.com", "password": "weak"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    client.assertIn(b"Please enter a valid password", response.data)

def test_login_route(client):
    """
    Tests the accessibility of the login route by making a GET request to 
    ensure the login page is accessible and rendered correctly.

    Returns:
        Asserts that the response status code is 200 and the 'login.html' 
        template is used.
    """
    response = client.client.get("/login")
    assert response.status_code == 200
    client.assert_template_used("login.html")
    client.assertIn(b"Login", response.data)

def test_login_valid_credentials(client):
    """
    Tests login functionality with valid credentials to ensure that users 
    can log in successfully and are redirected to their profile page.

    Returns:
        Asserts that the 'profile.html' template is used after a successful 
        login and redirection.
    """
    response = client.client.post(
        "/login",
        data={"email": "test@example.com", "password": "TestP@ssword!"},
        follow_redirects=False,
    )
    response = client.client.get(
        response.headers.get("Location"), follow_redirects=True
    )
    client.assert_template_used("profile.html")

def test_login_invalid_credentials(client):
    """
    Tests login functionality with invalid credentials to confirm system 
    correctly identifies incorrect login attempts and prevents access.

    Returns:
        Asserts that the response status code is 200, the 'login.html' 
        template is used, and an error message is displayed.
    """
    response = client.client.post(
        "/login",
        data={"email": "test@example.com", "password": "wrongpassword"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    client.assert_template_used("login.html")
    client.assertIn(
        b"Please check your login details and try again.", response.data
    )

def test_logout(client):
    """
    Tests the logout functionality to verify that a logged-in user can 
    successfully log out and is redirected to the home page.

    Returns:
        Asserts that after logging out, the response status code is 200 and 
        the 'home.html' template is used.
    """
    client.client.post(
        "/login",
        data={"email": "test@example.com", "password": "TestP@ssword!"},
        follow_redirects=True,
    )
    response = client.client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    client.assert_template_used("home.html")

def test_logout_not_logged_in(client):
    """
    Tests the logout route's behavior when no user is logged in. This test 
    ensures that the application handles unauthorized logout attempts 
    gracefully.

    Returns:
        Asserts that the response redirects to the login page, showing a 
        'login.html' template and a prompt to log in.
    """
    response = client.client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    client.assert_template_used("login.html")
    client.assertIn(b"Login", response.data)


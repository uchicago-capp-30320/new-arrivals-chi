"""
Project: New Arrivals Chi
File name: auth_basic.py
Associated Files:
    templates: signup.html, login.html, home.html, profile.html

This test suite performs basic validation of the user authorization routes
including signup, login, and logout functionalities for the New Arrivals
Chicago portal.

Methods:
    * test_signup_route
    * test_signup_post_invalid_email
    * test_signup_post_invalid_password
    * test_signup_post_valid_credentials
    * test_signup_post_weak_password
    * test_login_route
    * test_login_valid_credentials
    * test_login_invalid_credentials
    * test_logout
    * test_logout_not_logged_in

Last updated:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/08/2024

Creation:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/06/2024
"""


def test_signup_route(client, capture_templates):
    """
    Tests signup route by checking for correct response and template.
    """
    response = client.get("/signup")
    assert response.status_code == 200
    assert b"Sign Up" in response.data
    assert len(capture_templates) == 1
    assert capture_templates[0][0].name == "signup.html", "Wrong template used"


def test_signup_post_invalid_email(client, capture_templates):
    """
    Tests the signup with an invalid email format. Verifies that the system
    correctly identifies the email as invalid and returns to the signup page.
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
    assert len(capture_templates) == 1
    assert capture_templates[0][0].name == "signup.html", "Wrong template used"


def test_signup_post_invalid_password(client, capture_templates):
    """
    Tests the signup with an invalid password. Ensures that the application
    rejects passwords that do not meet the specified security criteria.
    """
    response = client.post(
        "/signup",
        data={
            "email": "test@example.com",  # invalid password
            "password": "password!",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Please enter a valid password" in response.data
    assert len(capture_templates) == 1
    assert capture_templates[0][0].name == "signup.html", "Wrong template used"


def test_signup_post_valid_credentials(client, capture_templates):
    """
    Tests the signup functionality with valid email and password.
    This test verifies if the application correctly handles valid
    registration credentials and redirects to the home page.
    """
    response = client.post(
        "/signup",
        data={
            "email": "new_user@example.com",  # valid email format
            "password": "StrongPassword123!",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert len(capture_templates) == 1
    assert capture_templates[0][0].name == "home.html", "Wrong template used"


def test_signup_post_weak_password(client, capture_templates):
    """
    Tests the signup functionality with a weak password to verify that the
    system enforces strong password requirements.
    """
    response = client.post(
        "/signup",
        data={"email": "new_user@example.com", "password": "weak"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Please enter a valid password" in response.data
    assert len(capture_templates) == 1
    assert capture_templates[0][0].name == "signup.html", "Wrong template used"


def test_login_route(client, capture_templates):
    """
    Tests the accessibility of the login route to  ensure the login page is
    accessible and rendered correctly.
    """
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data
    assert len(capture_templates) == 1
    assert capture_templates[0][0].name == "login.html", "Wrong template used"


def test_login_valid_credentials(client, capture_templates, test_user):
    """
    Tests login functionality with valid credentials to ensure that users
    can log in successfully and are redirected to their profile page.
    """
    response = client.post(
        "/login",
        data={"email": "test@example.com", "password": "TestP@ssword!"},
        follow_redirects=False,
    )
    response = client.get(
        response.headers.get("Location"), follow_redirects=True
    )
    assert response.status_code == 200
    assert len(capture_templates) == 1
    assert capture_templates[0][0].name == "profile.html", "Wrong template used"


def test_login_invalid_credentials(client, capture_templates):
    """
    Tests login functionality with invalid credentials to confirm system
    correctly identifies incorrect login attempts and prevents access.
    """
    response = client.post(
        "/login",
        data={"email": "test@example.com", "password": "wrongpassword"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Please check your login details and try again." in response.data
    assert len(capture_templates) == 1
    assert capture_templates[0][0].name == "login.html", "Wrong template used"


def test_logout(client, capture_templates, test_user, login_client):
    """
    Tests the logout functionality to verify that a logged-in user can
    successfully log out and is redirected to the home page.
    """
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert len(capture_templates) == 2
    assert capture_templates[1][0].name == "home.html", "Wrong template used"


def test_logout_not_logged_in(client, capture_templates):
    """
    Tests the logout route's behavior when no user is logged in. This test
    ensures that the application handles unauthorized logout attempts
    gracefully.
    """
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert len(capture_templates) == 1
    assert capture_templates[0][0].name == "login.html", "Wrong template used"

"""Project: New Arrivals Chi.

File name: csrf_protection_test.py

Associated Files:
    Templates: signup.html, login.html, change_password.html.

This test suite verifies the proper handling of CSRF tokens across various user authorization forms.
It ensures that all sensitive forms such as login, signup, and change password strictly enforce CSRF token validation, thereby protecting against CSRF attacks.
The suite tests for scenarios where forms should reject submissions without CSRF tokens, accept submissions with valid CSRF tokens, and reject submissions with invalid CSRF tokens.

Methods included:
    * test_login_form_rejection_without_csrf
    * test_login_form_acceptance_with_csrf
    * test_login_post_invalid_csrf
    * test_signup_form_rejection_without_csrf
    * test_signup_form_acceptance_with_csrf
    * test_signup_post_invalid_csrf
    * test_change_password_form_rejection_without_csrf
    * test_change_password_form_acceptance_with_csrf
    * test_change_password_post_invalid_csrf

Last updated:
@Author: Aaron Haefner @aaronhaefner
@Date: 2024-05-10

Creation:
@Author: Aaron Haefner @aaronhaefner
@Date: 2024-05-09
"""
from bs4 import BeautifulSoup
from utils import 




def test_login_form_rejection_without_csrf(client):
    """Verifies that submitting the login form without a CSRF token
    results in a rejection.

    Args:
        client: The test client for the application.

    Returns:
        None
    """
    response = client.post(
        "/login",
        data={"email": "user@example.com", "password": "securepassword"},
        follow_redirects=True,
    )
    assert (
        "The CSRF token is missing." in response.data.decode()
        or response.status_code == 400
    ), "Form should reject submission without CSRF token"


def test_login_form_acceptance_with_csrf(client, app):
    """Obtains a CSRF token by accessing the login page, then submits the login
    form with valid credentials and the retrieved CSRF token
    to verify successful submission.

    Args:
        client: The test client for the application.
        app: The application instance.

    Returns:
        None
    """
    # Get the login page to retrieve the CSRF token
    response = client.get("/login")
    csrf_token = get_csrf_token_from_response(response.data.decode())

    # Submit the form with CSRF token
    response = client.post(
        "/login",
        data={
            "email": "user@example.com",
            "password": "Str0ngP@$$word123!C0ntre$namUyfue&t3",
            "csrf_token": csrf_token,
        },
        follow_redirects=True,
    )
    assert (
        response.status_code == 200
    ), "Form should accept submission with valid CSRF token"


def test_login_post_invalid_csrf(client):
    """Attempts to submit the login form with an invalid CSRF
    token to verify that the form correctly rejects the submission.

    Args:
        client: The test client for the application.

    Returns:
        None
    """
    response = client.post(
        "/login",
        data={
            "email": "test@example.com",
            "password": "TestP@ssword!4234m!@3",
            "csrf_token": "invalid_csrf_token",
        },
        follow_redirects=True,
    )
    assert (
        "Invalid CSRF token. Please try again." in response.data.decode()
        or response.status_code == 400
    ), "Form should reject submission with invalid CSRF token"


def test_login_post_valid_csrf(client, test_user):
    """Submits the login form with a valid CSRF token
    to verify that the form accepts the submission.

    Args:
        client: The test client for the application.
        test_user: The test user instance.

    Returns:
        None
    """
    response = client.get("/login")
    csrf_token = get_csrf_token_from_response(response.data.decode())

    response = client.post(
        "/login",
        data={
            "email": "test@example.com",
            "password": "TestP@ss3fsadf3!@!@#",
            "csrf_token": csrf_token,
        },
        follow_redirects=True,
    )
    assert (
        response.status_code == 200
    ), "Form should accept submission with valid CSRF token"


def test_signup_form_rejection_without_csrf(client):
    """Verifies that submitting the signup form
    without a CSRF token results in a rejection.

    Args:
        client: The test client for the application.

    Returns:
        None
    """
    response = client.post(
        "/signup",
        data={
            "email": "test@example.com",
            "password": "TestP@ss35!@!@#daf3",
            "password_confirm": "TestP@ss35!@!@#daf3",
        },
        follow_redirects=True,
    )
    assert (
        "The CSRF token is missing." in response.data.decode()
        or response.status_code == 400
    ), "Form should reject submission without CSRF token"


def test_signup_form_acceptance_with_csrf(client):
    """Obtains a CSRF token by accessing the signup page, then submits the signup
    form with valid credentials and the retrieved CSRF token
    to verify successful submission.

    Args:
        client: The test client for the application.

    Returns:
        None
    """
    response = client.get("/signup")
    csrf_token = get_csrf_token_from_response(response.data.decode())

    response = client.post(
        "/signup",
        data={
            "email": "test@example.com",
            "password": "TestP@ss35!@!@#daf3",
            "password_confirm": "TestP@ss35!@!@#daf3",
            "csrf_token": csrf_token,
        },
        follow_redirects=True,
    )
    assert (
        response.status_code == 200
    ), "Form should accept submission with valid CSRF token"


def test_signup_post_invalid_csrf(client):
    """Attempts to submit the signup form with an invalid CSRF
    token to verify that the form correctly rejects the submission.

    Args:
        client: The test client for the application.

    Returns:
        None
    """
    response = client.post(
        "/signup",
        data={
            "email": "test@example.com",
            "password": "T$R%#@$FASD3m2o3sdf",
            "password_confirm": "T$R%#@$FASD3m2o3sdf",
            "csrf_token": "invalid_csrf_token",
        },
        follow_redirects=True,
    )
    assert (
        "Invalid CSRF token. Please try again." in response.data.decode()
        or response.status_code == 400
    ), "Form should reject submission with invalid CSRF token"


def test_signup_post_valid_csrf(client):
    """Submits the signup form with a valid CSRF token to verify
    that the form accepts the submission.

    Args:
        client: The test client for the application.

    Returns:
        None
    """
    response = client.get("/signup")
    csrf_token = get_csrf_token_from_response(response.data.decode())

    response = client.post(
        "/signup",
        data={
            "email": "test@example.com",
            "password": "T$R%#@$3o2m3v23lkmasdf",
            "password_confirm": "T$R%#@$3o2m3v23lkmasdf",
            "csrf_token": csrf_token,
        },
        follow_redirects=True,
    )


def test_change_password_form_rejection_without_csrf(client):
    """Verify that the change password form does not process
    submissions that lack a CSRF token.

    Args:
        client: The test client for the application.

    Returns:
        None
    """
    response = client.post(
        "/change_password",
        data={
            "old_password": "TestingP@ss35",
            "new_password": "NewTestingPsdf23r55",
            "new_password_confirm": "TestP@NewTestingPsdf23r55",
        },
        follow_redirects=True,
    )
    assert (
        "The CSRF token is missing." in response.data.decode()
        or response.status_code == 400
    ), "Submission without CSRF token should be rejected."


def test_change_password_form_acceptance_with_csrf(client):
    """Confirm that the change password form processes
    submissions correctly when a valid CSRF token is provided.

    Args:
        client: The test client for the application.

    Returns:
        None
    """
    response = client.get("/change_password")
    csrf_token = get_csrf_token_from_response(response.data.decode())

    response = client.post(
        "/change_password",
        data={
            "old_password": "TestingP@ss35",
            "new_password": "NewTestingPsdf23r55",
            "new_password_confirm": "NewTestingPsdf23r55",
            "csrf_token": csrf_token,
        },
        follow_redirects=True,
    )
    assert (
        response.status_code == 200
    ), "Form should correctly accept submissions with a valid CSRF token."


def test_change_password_post_invalid_csrf(client):
    """Test the change password form's ability to
    reject submissions with an invalid CSRF token.

    Args:
        client: The test client for the application.

    Returns:
        None
    """
    response = client.post(
        "/change_password",
        data={
            "old_password": "TestingP@ss35",
            "new_password": "NewTestingPsdf23r55",
            "new_password_confirm": "NewTestingPsdf23r55",
            "csrf_token": "invalid_csrf_token",
        },
        follow_redirects=True,
    )
    assert (
        "Invalid CSRF token. Please try again." in response.data.decode()
        or response.status_code == 400
    ), "Form should deny submissions with invalid CSRF tokens."


def test_change_password_post_valid_csrf(client):
    """Validate that the change password form accepts correctly submitted datawith a valid CSRF token.

    Args:
        client: The test client for the application.

    Returns:
        None
    """
    response = client.get("/change_password")
    csrf_token = get_csrf_token_from_response(response.data.decode())

    response = client.post(
        "/change_password",
        data={
            "old_password": "TestingP@ss35",
            "new_password": "NewTestingPsdf23r55",
            "new_password_confirm": "NewTestingPsdf23r55",
            "csrf_token": csrf_token,
        },
        follow_redirects=True,
    )
    assert (
        response.status_code == 200
    ), "Form must properly process valid submissions with a correct CSRF token."

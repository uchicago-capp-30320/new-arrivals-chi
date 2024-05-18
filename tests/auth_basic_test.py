"""Project: New Arrivals Chi.

File name: auth_basic.py
Associated Files:
    templates: signup.html, login.html, home.html, dashboard.html.

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
    * test_page_requiring_login_after_logout

Last updated:
@Author: Madeleine Roberts 05/09/2024
@Date: 05/08/2024

Creation:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/06/2024
"""

from http import HTTPStatus

from tests.constants import VALID_EMAIL, VALID_PASSWORD


def test_signup_route(client, capture_templates, setup_logger):
    """Tests the signup route.

    This test verifies that accessing the signup route returns the correct HTTP
    status,contains the expected 'Sign Up' text, and renders the appropriate
    template.

    Args:
        client: The test client used for making requests.
        capture_templates: Context manager to capture templates rendered.
        setup_logger: Setup logger.
    """
    logger = setup_logger("test_signup_route")
    try:
        response = client.get("/signup")
        assert response.status_code == 200
        assert b"Sign Up" in response.data, "Sign Up text not found in response"
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name == "signup.html"
        ), "Wrong template used"
        logger.info(
            "Signup page accessed successfully, correct template rendered."
        )
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_signup_post_invalid_email(client, capture_templates, setup_logger):
    """Tests the signup with an invalid email format.

    Verifies that the system
    correctly identifies the email as invalid and returns to the signup page.

    Args:
        client: The test client used for making requests.
        capture_templates: Context manager to capture templates rendered.
        setup_logger: Setup logger.
    """
    logger = setup_logger("test_signup_post_invalid_email")
    try:
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
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name == "signup.html"
        ), "Wrong template used"
        logger.info("Sign up failed successfully with invalid email.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_signup_post_invalid_password(client, capture_templates, setup_logger):
    """Tests the signup with an invalid password.

    Ensures that the application rejects passwords that do not meet the
    specified security criteria.

    Args:
        client: The test client used for making requests.
        capture_templates: Context manager to capture templates rendered.
        setup_logger: Setup logger.
    """
    logger = setup_logger("test_signup_post_invalid_password")
    try:
        response = client.post(
            "/signup",
            data={
                "email": "test@example.com",  # invalid password
                "password": "password!",
                "password_confirm": "password!",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Please enter a valid password" in response.data
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name == "signup.html"
        ), "Wrong template used"
        logger.info("Sign up failed successfully with invalid password.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_signup_post_weak_password(client, capture_templates, setup_logger):
    """Tests the signup functionality with a weak password.

    Verify that the system enforces strong password requirements.

    Args:
        client: The test client used for making requests.
        capture_templates: Context manager to capture templates rendered.
        setup_logger: Setup logger.
    """
    logger = setup_logger("test_signup_post_weak_password")
    try:
        response = client.post(
            "/signup",
            data={
                "email": "new_user123@example.com",
                "password": "weak",
                "password_confirm": "weak",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        print(response.data)
        assert b"Please enter a valid password" in response.data
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name == "signup.html"
        ), "Wrong template used"
        logger.info("Sign up failed successfully with weak password.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_login_route(client, capture_templates, setup_logger):
    """Tests the accessibility of the login route.

    Ensure the login page is accessible and rendered correctly.

    Args:
        client: The test client used for making requests.
        capture_templates: Context manager to capture templates rendered.
        setup_logger: Setup logger.
    """
    logger = setup_logger("test_login_route")
    try:
        response = client.get("/login")
        assert response.status_code == 200
        assert b"Login" in response.data
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name == "login.html"
        ), "Wrong template used"
        logger.info("Login page loaded successfully.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_login_valid_credentials(
    client, capture_templates, test_user, setup_logger
):
    """Tests login functionality with valid credentials.

    Ensure that users can log in successfully and are redirected to their
    dashboard page.

    Args:
        client: The test client used for making requests.
        capture_templates: Context manager to capture templates rendered.
        test_user: User instance for which the test is run.
        setup_logger: Setup logger.
    """
    logger = setup_logger("test_login_valid_credentials")
    try:
        response = client.post(
            "/login",
            data={"email": "test@example.com", "password": "TestP@ssword!"},
            follow_redirects=False,
        )
        response = client.get(
            response.headers.get("Location"), follow_redirects=True
        )
        assert response.status_code == 200
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name
            == "dashboard.html"
        ), "Wrong template used"
        logger.info("Login successfully with valid credentials.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_login_invalid_credentials(client, capture_templates, setup_logger):
    """Tests login functionality.

    Tests login functionality with invalid credentials to confirm system
    correctly identifies incorrect login attempts and prevents access.

    Args:
        client: The test client used for making requests.
        capture_templates: Context manager to capture templates rendered.
        setup_logger: Setup logger.
    """
    logger = setup_logger("test_login_invalid_credentials")
    try:
        response = client.post(
            "/login",
            data={"email": "test@example.com", "password": "wrongpassword"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert (
            b"Please check your login details and try again." in response.data
        )
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name == "login.html"
        ), "Wrong template used"
        logger.info("Login failed successfully with invalid credentials.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_logout(
    client, capture_templates, test_user, logged_in_state, setup_logger
):
    """Tests the logout functionality.

    Tests the logout functionality to verify that a logged-in user can
    successfully log out and is redirected to the home page.

    Args:
        client: The test client used for making requests.
        capture_templates: Context manager to capture templates rendered.
        test_user: User instance for which the test is run.
        logged_in_state: Session object for the logged-in client.
        setup_logger: Setup logger.
    """
    logger = setup_logger("test_logout")
    try:
        response = client.get("/logout", follow_redirects=True)
        assert response.status_code == 200
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name == "home.html"
        ), "Wrong template used"
        logger.info("Successful logout.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_logout_not_logged_in(client, capture_templates, setup_logger):
    """Tests the logout route's behavior when no user is logged in.

    This test ensures that the application handles unauthorized logout attempts
    gracefully.

    Args:
        client: The test client used for making requests.
        capture_templates: Context manager to capture templates rendered.
        setup_logger: Setup logger.
    """
    logger = setup_logger("test_logout_not_logged_in")
    try:
        response = client.get("/logout", follow_redirects=True)
        assert response.status_code == 200
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name == "login.html"
        ), "Wrong template used"
        logger.info("Successful redirect on invalid logout.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_page_requiring_login_after_logout(
    client, capture_templates, setup_logger
):
    """Tests behavior accessing page that requires login after user logged out.

    This test ensures that the application redirects to the login page when an
    unauthenticated user attempts to access a restricted page (e.g., the
    dashboard page) after logging out.

    Args:
        client: The test client used for making requests.
        capture_templates: Context manager to capture templates rendered.
        setup_logger: Setup logger.
    """
    logger = setup_logger("test_page_requiring_login_after_logout")
    client.post(
        "/login",
        data={"email": VALID_EMAIL, "password": VALID_PASSWORD},
        follow_redirects=True,
    )
    client.get("/logout", follow_redirects=True)

    try:
        dashboard_response = client.get("/dashboard", follow_redirects=True)
        assert dashboard_response.status_code == HTTPStatus.OK
        assert (
            b"Login" in dashboard_response.data
        ), "User not prompted to log in"
        assert len(capture_templates) == 3
        assert (
            capture_templates[2][0].name == "login.html"
        ), "Did not redirect to login page after trying to access dashboard"
        logger.info("Successful redirect to login page.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise

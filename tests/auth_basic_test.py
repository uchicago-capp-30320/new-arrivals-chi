"""Project: New Arrivals Chi.

File name: auth_basic.py
Associated Files:
    templates: signup.html, login.html, home.html, profile.html.

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


def test_signup_route(client, capture_templates, setup_logger):
    """Tests the signup route.

    This test verifies that accessing the signup route returns the correct HTTP
    status,contains the expected 'Sign Up' text, and renders the appropriate
    template.
    """
    logger = setup_logger("test_signup_route")
    try:
        response = client.get("/signup")
        assert response.status_code == 200
        assert b"Sign Up" in response.data, "Sign Up text not found in response"
        assert len(capture_templates) == 1
        assert (
            capture_templates[0][0].name == "signup.html"
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
        assert (
            capture_templates[0][0].name == "signup.html"
        ), "Wrong template used"
        logger.info("Sign up failed successfully with invalid email.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_signup_post_invalid_password(client, capture_templates, setup_logger):
    """Tests the signup with an invalid password.

    Ensures that the application rejects passwords that do not meet the
    specified security criteria.
    """
    logger = setup_logger("test_signup_post_invalid_password")
    try:
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
        assert (
            capture_templates[0][0].name == "signup.html"
        ), "Wrong template used"
        logger.info("Sign up failed successfully with invalid password.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_signup_post_valid_credentials(client, capture_templates, setup_logger):
    """Tests the signup functionality with valid email and password.

    This test verifies if the application correctly handles valid
    registration credentials and redirects to the home page.
    """
    logger = setup_logger("test_signup_post_valid_credentials")
    try:
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
        assert (
            capture_templates[0][0].name == "home.html"
        ), "Wrong template used"
        logger.info("Sign up successful with valid credentials.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_signup_post_weak_password(client, capture_templates, setup_logger):
    """Tests the signup functionality with a weak password.

    Verify that the system enforces strong password requirements.
    """
    logger = setup_logger("test_signup_post_weak_password")
    try:
        response = client.post(
            "/signup",
            data={"email": "new_user@example.com", "password": "weak"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Please enter a valid password" in response.data
        assert len(capture_templates) == 1
        assert (
            capture_templates[0][0].name == "signup.html"
        ), "Wrong template used"
        logger.info("Sign up failed successfully with weak password.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_login_route(client, capture_templates, setup_logger):
    """Tests the accessibility of the login route.

    Ensure the login page is accessible and rendered correctly.
    """
    logger = setup_logger("test_login_route")
    try:
        response = client.get("/login")
        assert response.status_code == 200
        assert b"Login" in response.data
        assert len(capture_templates) == 1
        assert (
            capture_templates[0][0].name == "login.html"
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
    profile page.
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
        assert len(capture_templates) == 1
        assert (
            capture_templates[0][0].name == "profile.html"
        ), "Wrong template used"
        logger.info("Login successfully with valid credentials.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_login_invalid_credentials(client, capture_templates, setup_logger):
    """Tests login functionality.

    Tests login functionality with invalid credentials to confirm system
    correctly identifies incorrect login attempts and prevents access.
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
        assert len(capture_templates) == 1
        assert (
            capture_templates[0][0].name == "login.html"
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
    """
    logger = setup_logger("test_logout")
    try:
        response = client.get("/logout", follow_redirects=True)
        assert response.status_code == 200
        assert len(capture_templates) == 2
        assert (
            capture_templates[1][0].name == "home.html"
        ), "Wrong template used"
        logger.info("Successful logout.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_logout_not_logged_in(client, capture_templates, setup_logger):
    """Tests the logout route's behavior when no user is logged in.

    This test ensures that the application handles unauthorized logout attempts
    gracefully.
    """
    logger = setup_logger("test_logout_not_logged_in")
    try:
        response = client.get("/logout", follow_redirects=True)
        assert response.status_code == 200
        assert len(capture_templates) == 1
        assert (
            capture_templates[0][0].name == "login.html"
        ), "Wrong template used"
        logger.info("Successful redirect on invalid logout.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise

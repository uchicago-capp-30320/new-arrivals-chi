"""Project: New Arrivals Chi.

File name: auth_change_password_test.py

Associated Files:
    Templates: change_password.html, login.html, profile.html.

This test suite verifies the functionality of the change password feature,
including testing various scenarios such as incorrect old password,
new password validation, password confirmation mismatch, and successful
password change.

Methods:
    * test_access_change_password_page
    * test_change_password_wrong_old_password
    * test_change_password_wrong_new_password_same_as_old
    * test_change_password_new_passwords_do_not_match
    * test_change_password_new_password_invalid
    * test_change_password_success

Last updated:
@Author: Madeleine Roberts @madeleinekroberts
@Date: 05/09/2024

Creation:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/07/2024
"""


def test_access_change_password_page(
    client, capture_templates, test_user, logged_in_state, setup_logger
):
    """Test Access Change Password Page.

    Verifies that the change password page is accessible.
    Ensures that the correct template is rendered when accessing this page.

    Args:
        client: The test client used for making requests.
        capture_templates: Context manager to capture templates rendered.
        test_user: User instance for which the test is run.
        logged_in_state: Session object for the logged-in client.
        setup_logger: Setup logger.
    """
    logger = setup_logger("test_access_change_password_page")
    try:
        response = client.get("/change_password", follow_redirects=True)
        assert response.status_code == 200
        assert len(capture_templates) == 2
        assert (
            capture_templates[1][0].name == "change_password.html"
        ), "Wrong template used"
        logger.info("Change password page rendered correctly.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_change_password_wrong_old_password(
    client, capture_templates, test_user, logged_in_state, setup_logger
):
    """Tests change password functionality with an incorrect old password.

    This should not allow the user to change the password, and the same page
    should be re-rendered with an error message.

    Args:
        client: The test client used for making requests.
        capture_templates: Context manager to capture templates rendered.
        test_user: User instance for which the test is run.
        logged_in_state: Session object for the logged-in client.
        setup_logger: Setup logger.
    """
    logger = setup_logger("test_change_password_wrong_old_password")
    try:
        response = client.post(
            "/change_password",
            data={
                "old_password": "BestP@ssword!",
                "new_password": "TestP@ssword!_2!",
                "new_password_confirm": "TestP@ssword!_2!",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Wrong existing password. Try again" in response.data
        assert len(capture_templates) == 2
        assert (
            capture_templates[1][0].name == "change_password.html"
        ), "Wrong template used"
        logger.info(
            "Change password successfully failed due to wrong old password."
        )
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_change_password_wrong_new_password_same_as_old(
    client, capture_templates, test_user, logged_in_state, setup_logger
):
    """Tests change password functionality with the new password same as old.

    The user should receive an error stating that the new password
    cannot be the same as the old password.

    Args:
        client: The test client used for making requests.
        capture_templates: Context manager to capture templates rendered.
        test_user: User instance for which the test is run.
        logged_in_state: Session object for the logged-in client.
        setup_logger: Setup logger.
    """
    logger = setup_logger("test_change_password_wrong_new_password_same_as_old")
    try:
        response = client.post(
            "/change_password",
            data={
                "old_password": "TestP@ssword!",
                "new_password": "TestP@ssword!",
                "new_password_confirm": "TestP@ssword!",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert (
            b"New password cannot be the same as your previous password."
            in response.data
        )
        assert len(capture_templates) == 2
        assert (
            capture_templates[1][0].name == "change_password.html"
        ), "Wrong template used"
        logger.info(
            "Change password successfully failed - new password same as old."
        )
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_change_password_new_passwords_do_not_match(
    client, capture_templates, test_user, logged_in_state, setup_logger
):
    """Tests change password functionality with mismatched new password.

    This should result in an error message prompting the user to
    ensure passwords match.

    Args:
        client: The test client used for making requests.
        capture_templates: Context manager to capture templates rendered.
        test_user: User instance for which the test is run.
        logged_in_state: Session object for the logged-in client.
        setup_logger: Setup logger.
    """
    logger = setup_logger("test_change_password_wrong_new_password_same_as_old")
    try:
        response = client.post(
            "/change_password",
            data={
                "old_password": "TestP@ssword!",
                "new_password": "TestP@ssword!_2!",
                "new_password_confirm": "BestP@ssword!_2!",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"New passwords do not match. Try again." in response.data
        assert len(capture_templates) == 2
        assert (
            capture_templates[1][0].name == "change_password.html"
        ), "Wrong template used"
        logger.info(
            "Change password successfully failed - passwords don't match."
        )
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_change_password_new_password_invalid(
    client, capture_templates, test_user, logged_in_state, setup_logger
):
    """Tests change password functionality with insecure new password.

    This should re-render the page with an error message regarding password
    requirements.

    Args:
        client: The test client used for making requests.
        capture_templates: Context manager to capture templates rendered.
        test_user: User instance for which the test is run.
        logged_in_state: Session object for the logged-in client.
        setup_logger: Setup logger.
    """
    logger = setup_logger("test_change_password_new_password_invalid")
    try:
        response = client.post(
            "/change_password",
            data={
                "old_password": "TestP@ssword!",
                "new_password": "badpassword",
                "new_password_confirm": "badpassword",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert (
            b"New password does not meet requirements. Try again."
            in response.data
        )
        assert len(capture_templates) == 2
        assert (
            capture_templates[1][0].name == "change_password.html"
        ), "Wrong template used"
        logger.info(
            "Change password successfully failed due to invalid new password."
        )
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


def test_change_password_success(
    client, test_user, logged_in_state, capture_templates, setup_logger
):
    """Verifies the successful change of a user's password.

    Complete flow of changing the password, logging out, and then logging back
    in with the new password.This test ensures that all steps in the password
    change process work correctly together.

    Args:
        client: The test client used for making requests.
        test_user: User instance for which the test is run.
        logged_in_state: Session object for the logged-in client.
        capture_templates: Context manager to capture templates.
        setup_logger: Setup logger.
    """
    logger = setup_logger("test_change_password_success")
    try:
        old_password = "TestP@ssword!"
        new_password = "cH@^v6EDStr0ngP@$$word123!C0ntre$namUyfue&t3"

        # change password
        response = client.post(
            "/change_password",
            data={
                "old_password": old_password,
                "new_password": new_password,
                "new_password_confirm": new_password,
            },
            follow_redirects=True,
        )
        assert response.status_code == 200

        # logout
        client.get("/logout", follow_redirects=True)

        # try to log in with the new password
        response = client.post(
            "/login",
            data={"email": test_user.email, "password": new_password},
            follow_redirects=True,
        )

        # if the login is successful, password was changed correctly
        assert response.status_code == 200
        assert b"Profile" in response.data
        assert len(capture_templates) == 3
        assert (
            capture_templates[2][0].name == "profile.html"
        ), "Wrong template used"
        logger.info("Change password successful.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise

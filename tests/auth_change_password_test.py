"""Project: New Arrivals Chi.

File name: auth_change_password_test.py

Associated Files:
    Templates: change_password.html, login.html, dashboard.html.

This test suite verifies the functionality of the change password feature,
including testing various scenarios such as incorrect old password,
new password validation, password confirmation mismatch, and successful
password change.

Methods:
    * test_access_change_password_page
    * test_change_password_scenarios
    * test_change_password_success
"""

import pytest
from http import HTTPStatus

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
        assert response.status_code == HTTPStatus.OK
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name
            == "change_password.html"
        ), "Wrong template used"
        logger.info("Change password page rendered correctly.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise


@pytest.mark.parametrize(
    "old_password, new_password, new_password_confirm, expected_message",
    [
        ("BestP@ssword!", "TestP@ssword!_2!", "TestP@ssword!_2!", b"Wrong existing password. Try again"),
        ("TestP@ssword!", "TestP@ssword!", "TestP@ssword!", b"New password cannot be the same as your previous password."),
        ("TestP@ssword!", "TestP@ssword!_2!", "BestP@ssword!_2!", b"New passwords do not match. Try again."),
        ("TestP@ssword!", "badpassword", "badpassword", b"New password does not meet requirements. Try again."),
    ]
)
def test_change_password_scenarios(
    client, capture_templates, test_user, logged_in_state, setup_logger,
    old_password, new_password, new_password_confirm, expected_message
):
    """Tests various scenarios for changing password.

    Args:
        client: The test client used for making requests.
        capture_templates: Context manager to capture templates rendered.
        test_user: User instance for which the test is run.
        logged_in_state: Session object for the logged-in client.
        setup_logger: Setup logger.
        old_password: The current password of the user.
        new_password: The new password to be set.
        new_password_confirm: The confirmation of the new password.
        expected_message: The expected message to be found in the response.
    """
    logger = setup_logger("test_change_password_scenarios")
    try:
        response = client.post(
            "/change_password",
            data={
                "old_password": old_password,
                "new_password": new_password,
                "new_password_confirm": new_password_confirm,
            },
            follow_redirects=True,
        )
        assert response.status_code == HTTPStatus.OK
        assert expected_message in response.data
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name
            == "change_password.html"
        ), "Wrong template used"
        logger.info(f"Change password scenario processed with expected message: {expected_message}")
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
        assert response.status_code == HTTPStatus.OK

        # logout
        client.get("/logout", follow_redirects=True)

        # try to log in with the new password
        response = client.post(
            "/login",
            data={"email": test_user.email, "password": new_password},
            follow_redirects=True,
        )

        # if the login is successful, password was changed correctly
        assert response.status_code == HTTPStatus.OK
        assert b"dashboard" in response.data
        final_template_rendered = len(capture_templates) - 1
        assert (
            capture_templates[final_template_rendered][0].name
            == "dashboard.html"
        ), "Wrong template used"
        logger.info("Change password successful.")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
        raise

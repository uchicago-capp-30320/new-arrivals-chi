"""
Project: New Arrivals Chi
File name: auth_change_password_test.py
Associated Files:
    Templates: change_password.html, login.html, profile.html

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
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/08/2024

Creation:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/07/2024
"""


def test_access_change_password_page(
    client, capture_templates, test_user, login_client
):
    """
    Tests that change password page can be reached.
    """
    response = client.get("/change_password", follow_redirects=True)
    assert response.status_code == 200
    assert len(capture_templates) == 2
    assert (
        capture_templates[1][0].name == "change_password.html"
    ), "Wrong template used"


def test_change_password_wrong_old_password(
    client, capture_templates, test_user, login_client
):
    response = client.post(
        "/change_password",
        data={
            "old_password": "BestP@ssword!",
            "new_password": "TestP@ssword!_2!",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Wrong existing password. Try again" in response.data
    assert len(capture_templates) == 2
    assert (
        capture_templates[1][0].name == "change_password.html"
    ), "Wrong template used"


def test_change_password_wrong_new_password_same_as_old(
    client, capture_templates, test_user, login_client
):
    response = client.post(
        "/change_password",
        data={
            "old_password": "TestP@ssword!",
            "new_password": "TestP@ssword!",
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


def test_change_password_new_passwords_do_not_match(
    client, capture_templates, test_user, login_client
):
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


def test_change_password_new_password_invalid(
    client, capture_templates, test_user, login_client
):
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
        b"New password does not meet requirements. Try again." in response.data
    )
    assert len(capture_templates) == 2
    assert (
        capture_templates[1][0].name == "change_password.html"
    ), "Wrong template used"


def test_change_password_success(
    client, test_user, login_client, capture_templates
):
    """
    Verifies that the password change functionality works correctly by changing
    the password and then logging in with updated credentials.
    """
    old_password = "TestP@ssword!"
    new_password = "TestP@ssword!-2!"

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
    assert capture_templates[2][0].name == "profile.html", "Wrong template used"

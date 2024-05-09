"""Project: New Arrivals Chi.

File name: auth_security_test.py

Associated Files:
   Templates: signup.html, login.html
   Utils: validate_password.

This test suite performs more robust security testing for user authorization
routes and password handling mechanisms for the New Arrivals Chicago portal.

Methods:
   * test_set_up_password_hashed
   * test_set_up_all_password_params
   * test_password_never_logged_plaintext

Last updated:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/08/2024

Creation:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/06/2024
"""

from new_arrivals_chi.app.database import User
from werkzeug.security import check_password_hash
from new_arrivals_chi.app.utils import validate_password
from unittest.mock import patch


def test_set_up_password_hashed(test_user):
    """Tests that the password stored in the database is correctly hashed."""
    user = User.query.filter_by(email="test@example.com").first()
    assert check_password_hash(user.password, "TestP@ssword!")


def test_set_up_all_password_params():
    """Test passwords that each violate only one of the requirements.

    Requirements tested: 8+ characters, 1+ number, 1+ special characters, not
    empty, no spaces.
    """
    # test password with less than 8 characters
    short_password = "pA4s!12"
    assert not validate_password(short_password)

    # test password without a number
    no_number = "password@#$%"
    assert not validate_password(no_number)

    # test password without a special character
    no_special_char = "password123456"
    assert not validate_password(no_special_char)

    # test empty password
    empty_password = ""
    assert not validate_password(empty_password)

    # test password with spaces
    password_with_spaces = "password 123!@#"
    assert not validate_password(password_with_spaces)


def test_password_never_logged_plaintext(client, setup_logger):
    """Check that logger never stores plain text password."""
    logger = setup_logger("test_logger")

    # attempt to sign up a new user
    with patch.object(logger, "info") as mock_logger:
        client.post(
            "/signup",
            data={"email": "test2@example.com", "password": "TestPassword123!"},
        )

        # check that the plain text password is not present in the logs
        for log_call in mock_logger.call_args_list:
            args, _ = log_call
            assert "TestPassword123!" not in "".join(args)

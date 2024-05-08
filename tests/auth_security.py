"""
Project: New Arrivals Chi
File name: auth_security.py
Associated Files:


This test suite performs more robust security testing for user authorization
routes for the New Arrivals Chicago portal.

Methods:

Last updated:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/06/2024

Creation:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/06/2024
"""

from flask_testing import TestCase
from new_arrivals_chi.app.main import create_app, db
from new_arrivals_chi.app.database import User
from werkzeug.security import generate_password_hash, check_password_hash
import re

    
def test_set_up_password_hashed(self):
    """
    Tests that the password stored in the database is correctly hashed.
    """
    user = User.query.filter_by(email="test@example.com").first()
    self.assertTrue(check_password_hash(user.password, "TestP@ssword!"))


def test_set_up_all_password_params(self):
    """
    TODO: test passwords that each violate only one of the requirements
    - 8+ characters
    - 1+ number,
    - 1+ special characters
    - empty
    - excluded special chars
    - spaces
    """

def test_password_never_logged_plaintext(self):
    """
    TODO: check that logger never stores plain text password
    """

def test_login_attemts(self):
    """
    TODO: check that system limits login attempts
    """

def test_password_reset_unique_link(self):
    """
    TODO: verify password reset links are single use,
    """

def test_set_up_sanitized_username(self):
    """
    TODO: make sure username is sanitized on set-up
    """

def test_set_up_sanitized_password(self):
    """
    TODO: make sure password is sanitized on set-up
    """

def test_login_sanitized_username(self):
    """
    TODO: make sure username is sanitized on login
    """

def test_login_sanitized_password(self):
    """
    TODO: make sure password is sanitized on login
    """

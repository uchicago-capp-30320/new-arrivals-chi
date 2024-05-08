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


class TestAuthorizeRoutes(TestCase):
    def create_app(self):
        """
        Sets up a Flask application configured for testing.
        The application is configured to use a memory-based SQLite database
        and a secret key for session management.

        Returns:
            Flask app instance with test configurations.
        """
        app = create_app()
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.secret_key = "test_secret_key"
        return app

    def setUp(self):
        """
        Prepares the testing environment before each test.
        This includes creating the database tables and adding a test user with
        a hashed password.
        """
        db.create_all()
        hashed_password = generate_password_hash(
            "TestP@ssword!", method="pbkdf2:sha256"
        )
        self.test_user = User(
            email="test@example.com", password=hashed_password
        )
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        """
        Cleans up the testing environment after each test by removing the
        database tables.
        """
        db.session.remove()
        db.drop_all()

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

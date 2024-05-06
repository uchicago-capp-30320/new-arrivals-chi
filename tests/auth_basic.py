"""
Project: New Arrivals Chi
File name: auth_basic.py
Associated Files:
    new_arrivals_chi/app/main.py,
    new_arrivals_chi/app/database.py,
    templates: signup.html, login.html, home.html, profile.html

This test suite performs basic validation of the user authorization routes
including signup, login, and logout functionalities for the New Arrivals
Chicago portal.

Methods:
    * test_create_app — Sets up the Flask application for testing.
    * test_set_up — Prepares the database and a test user before each test.
    * test_tear_down — Cleans up the database after each test.
    * test_signup_route — Tests the accessibility of the signup route.
    * test_signup_post_invalid_email — Tests signup with an invalid email.
    * test_signup_post_invalid_password — Tests signup with an invalid password.
    * test_signup_post_valid_credentials — Tests signup with valid credentials.
    * test_signup_post_weak_password — Tests signup with a weak password.
    * test_login_route — Tests the accessibility of the login route.
    * test_login_valid_credentials — Tests login with valid credentials.
    * test_login_invalid_credentials — Tests login with invalid credentials.
    * test_logout — Tests the logout functionality.
    * test_logout_not_logged_in — Tests the logout route when no user logged in.

Last updated:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/06/2024

Creation:
@Author: Kathryn Link-Oberstar @klinkoberstar
@Date: 05/06/2024
"""

import pytest
from flask_testing import TestCase
from new_arrivals_chi.app.main import create_app, db
from new_arrivals_chi.app.database import User
from werkzeug.security import generate_password_hash


class TestAuthorizeRoutes(TestCase):
    def test_create_app(self):
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

    def test_set_up(self):
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

    def test_tear_down(self):
        """
        Cleans up the testing environment after each test by removing the
        database tables.
        """
        db.session.remove()
        db.drop_all()

    def test_signup_route(self):
        """
        Tests the accessibility of the signup route by making a GET request
        and verifying the response.

        Returns:
            Asserts that the response status code is 200 and the correct
            template 'signup.html' is used.
        """
        response = self.client.get("/signup")
        self.assert200(response)
        self.assert_template_used("signup.html")
        self.assertIn(b"Sign Up", response.data)

    def test_signup_post_invalid_email(self):
        """
        Tests the signup functionality with an invalid email format. Verifies
        that the system correctly identifies the email as invalid and returns
        to the signup page.

        Returns:
            Asserts that the response status code is 200, the correct template
            'signup.html' is used, and an appropriate error message is included
            in the response.
        """
        response = self.client.post(
            "/signup",
            data={
                "email": "bad_email",  # invalid email format
                "password": "TestP@ssword!",
            },
            follow_redirects=True,
        )
        self.assert200(response)
        self.assert_template_used("signup.html")
        self.assertIn(b"Please enter a valid email address", response.data)

    def test_signup_post_invalid_password(self):
        """
        Tests the signup functionality with an invalid password. Ensures that
        the application rejects passwords that do not meet the specified
        security criteria.

        Returns:
            Asserts that the response status code is 200, the 'signup.html'
            template is used, and an appropriate error message is displayed.
        """
        response = self.client.post(
            "/signup",
            data={
                "email": "test@example.com",  # invalid password
                "password": "password!",
            },
            follow_redirects=True,
        )
        self.assert200(response)
        self.assert_template_used("signup.html")
        self.assertIn(b"Please enter a valid password", response.data)

    def test_signup_post_valid_credentials(self):
        """
        Tests the signup functionality with valid email and password.
        This test verifies if the application correctly handles valid
        registration credentials and redirects to the home page.

        Returns:
            Asserts that the response status code is 200, the 'home.html'
            template is used after successful signup.
        """
        response = self.client.post(
            "/signup",
            data={
                "email": "new_user@example.com",  # valid email format
                "password": "StrongPassword123!",
            },
            follow_redirects=True,
        )
        self.assert200(response)
        self.assert_template_used("home.html")

    def test_signup_post_weak_password(self):
        """
        Tests the signup functionality with a weak password to verify that the
        system enforces strong password requirements.

        Returns:
            Asserts that the response status code is 200, the 'signup.html'
            template is reused, and an error message regarding password strength
            is displayed.
        """
        response = self.client.post(
            "/signup",
            data={"email": "new_user@example.com", "password": "weak"},
            follow_redirects=True,
        )
        self.assert200(response)
        self.assert_template_used("signup.html")
        self.assertIn(b"Please enter a valid password", response.data)

    def test_login_route(self):
        """
        Tests the accessibility of the login route by making a GET request to
        ensure the login page is accessible and rendered correctly.

        Returns:
            Asserts that the response status code is 200 and the 'login.html'
            template is used.
        """
        response = self.client.get("/login")
        self.assert200(response)
        self.assert_template_used("login.html")
        self.assertIn(b"Login", response.data)

    def test_login_valid_credentials(self):
        """
        Tests login functionality with valid credentials to ensure that users
        can log in successfully and are redirected to their profile page.

        Returns:
            Asserts that the 'profile.html' template is used after a successful
            login and redirection.
        """
        response = self.client.post(
            "/login",
            data={"email": "test@example.com", "password": "TestP@ssword!"},
            follow_redirects=False,
        )
        response = self.client.get(
            response.headers.get("Location"), follow_redirects=True
        )
        self.assert_template_used("profile.html")

    def test_login_invalid_credentials(self):
        """
        Tests login functionality with invalid credentials to confirm system
        correctly identifies incorrect login attempts and prevents access.

        Returns:
            Asserts that the response status code is 200, the 'login.html'
            template is used, and an error message is displayed.
        """
        response = self.client.post(
            "/login",
            data={"email": "test@example.com", "password": "wrongpassword"},
            follow_redirects=True,
        )
        self.assert200(response)
        self.assert_template_used("login.html")
        self.assertIn(
            b"Please check your login details and try again.", response.data
        )

    def test_logout(self):
        """
        Tests the logout functionality to verify that a logged-in user can
        successfully log out and is redirected to the home page.

        Returns:
            Asserts that after logging out, the response status code is 200 and
            the 'home.html' template is used.
        """
        self.client.post(
            "/login",
            data={"email": "test@example.com", "password": "TestP@ssword!"},
            follow_redirects=True,
        )
        response = self.client.get("/logout", follow_redirects=True)
        self.assert200(response)
        self.assert_template_used("home.html")

    def test_logout_not_logged_in(self):
        """
        Tests the logout route's behavior when no user is logged in. This test
        ensures that the application handles unauthorized logout attempts
        gracefully.

        Returns:
            Asserts that the response redirects to the login page, showing a
            'login.html' template and a prompt to log in.
        """
        response = self.client.get("/logout", follow_redirects=True)
        self.assert200(response)
        self.assert_template_used("login.html")
        print(response.data)
        self.assertIn(b"Login", response.data)


if __name__ == "__main__":
    pytest.main()

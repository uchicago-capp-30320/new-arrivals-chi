# Flask Application Testing Documentation

## Testing Framework

We utilize `pytest` along with the `pytest-flask` plugin to facilitate our testing.

### Configuration with `conftest.py`

The core configurations for our tests are managed through `conftest.py`, which includes fixtures that can be used across multiple test files.

#### Fixtures Provided

- `app`: Configures and provides the Flask application instance, testing enabled.
- `client`: Provides a test client for the application.
- `database`: Provides a test database instance for the application.
- `setup_logger`: Provides an instance to log test results.
- `capture_templates`: Captures the templates rendered during a test.
- `test_user`: Creates a test user in the database before each test and removes it after.
- `logged_in_state`: Logs in a user for testing routes that require authentication.

## Writing Tests

Test files are organized by their respective application components.

### Authentication and Security Tests

The `auth_basic.py` file contains tests for basic authentication operations such as signup, login, and logout.

#### Tests Included

- **Signup Route Access**: Verifies the accessibility and template rendering of the signup page.
- **Signup with Invalid Data**: Ensures proper handling of invalid emails, passwords, and SQL injection attempts during signup.
- **Signup with Weak Password**: Verifies that the system enforces strong password requirements.
- **Login Route Access**: Verifies the accessibility and template rendering of the login page.
- **Login with Valid Credentials**: Tests successful login and template rendering for valid users.
- **Login with Invalid Credentials**: Ensures proper handling of incorrect login attempts, including SQL injection attempts.
- **Logout**: Verifies successful logout and correct template rendering.
- **Logout When Not Logged In**: Ensures proper handling of logout attempts when no user is logged in.
- **Page Requiring Login After Logout**: Ensures proper redirection to login for unauthenticated access attempts to protected pages.

The `auth_security_test.py` file focuses on password handling and security.

#### Tests Included

- **Password Hashing**: Ensures that passwords are stored hashed in the database.
- **Password Requirements**: Verifies that passwords meet specific security criteria (length, numbers, special characters, no spaces).
- **Logger Security**: Ensures that plaintext passwords are never stored in logs.

The `auth_change_password_test.py` file contains tests for changing passwords.

#### Tests Included

- **Access Change Password Page**: Verifies accessibility and correct template rendering of the change password page.
- **Change Password Scenarios**: Ensures proper handling of incorrect old passwords, new passwords that match old ones, mismatched new passwords, and insecure new passwords.
- **Successful Password Change**: Verifies the complete flow of changing a password, logging out, and logging back in with the new password.

### Legal Routes Tests

The `legal_routes_test.py` file contains tests for legal information routes, ensuring proper access and correct template rendering.

#### Tests Included

- **Access Legal Page**: Verifies the accessibility and template rendering of the legal page.
- **Access Various Legal Routes**: Ensures proper access and correct template rendering for:
TPS, VTTC, Asylum, Parole, Undocumented Resources, Legal Help, Workers' Rights, and Renters' Rights pages.

### Database Operation Tests

The `utils.py` file contains functions for creating the fake database.
The `setup_fake_db.py` script is used to create a fake database instance and fill it with data.

#### Tests Included

- **Fake Data Creation**: Confirms that users, organizations, locations, and hours can be created, added to sessions, and committed without issues.
- **Data Retrieval**: Tests retrieving users by their ID and asserts the correctness of the data like email format and user roles.
- **Data Validation**: Verifies the integrity of data relationships, ensuring that users are linked to valid organizations and all entities have expected attributes.
- **Authentication**: Tests to check authentication pathways including sign-up, login, logout, password changes, and password security.
- **Error Handling and Logging**: Logs errors during data creation and handles exceptions with rollback.
- **Prevention of SQL Injections**: Tests for secure handling of safe and unsafe inputs within the fake database instance, preventing malicious actions such as returning all records or dropping tables.

### Additional Tests - In Progress

## Running Tests

### Commands

Here's how to run all tests and specific tests:

- **Run all tests**:
  ```bash
  poetry run pytest
  ```
- **Run a specific test**:
  ```bash
  poetry run pytest tests/app_home_test.py::test_home_page_status
  ```
- **Run database tests**:
  ```bash
  poetry run pytest tests/db_test.py
  ```

## Contributing

### Guidelines

- **Adding Tests**: When adding new features, include comprehensive tests that cover both new functionalities and their integration into existing features (code writer or QA).
- **Existing Tests**: Ensure code modifications are backward compatible where possible and that they do not break existing tests (code writer).
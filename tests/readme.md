# Flask Application Testing Documentation

## Testing Framework

We utilize `pytest` along with the `pytest-flask` plugin to facilitate our testing.  

### Configuration with `conftest.py`

The core configurations for our tests are managed through `conftest.py`, which includes fixtures that can be used across multiple test files.

#### Fixtures Provided

- `app`: Configures and provides the Flask application instance, testing enabled
- `client`: Provides a test client for the application
- `database`: Provides a test database instance for the application
- `logger`: Provides an instance to log test results
- `capture_templates`: Create a function to retrieve the templates rendered
- `test_user`: Create a test user in the database before each test and remove after
- `logged_in_state`(client): Logs in a user for testing routes that require authentication

## Writing Tests

Test files are organized by their respective application components.

## Database Operation Tests

The `db_test.py` file focuses on testing database operations and consistency across our application.
It utilizes fixtures for the app, logger, and database and ensures all tests run within the application context.

The `setup_fake_db.py` script is used to create a fake database instance and fill it with fake data.

### Tests Included

- **Fake Data Creation**: Confirms that users, organizations, locations, and hours can be created, added to sessions, and committed without issues.
- **Data Retrieval**: Tests retrieving users by their ID and asserts the correctness of the data like email format and user roles.
- **Data Validation**: Verifies the integrity of data relationships, ensuring that users are linked to valid organizations and all entities have expected attributes.
- **Authentication**: Tests to check authentication pathways including sign-up, login, logout, password changes, and password security.
- **Error Handling and Logging**: Log errors during data creation and handle exceptions with rollback.

## Cross Site Request Forgery (CSRF) Tests

Cross Site Request Forgery (CSRF) is a type of attack where a malicious website sends a request to a different website on behalf of a user.
This can lead to unauthorized actions being performed on the user's behalf, such as changing passwords or making purchases.

To ensure application security, we have implemented a series of CSRF protection tests.
These tests verify that our application properly handles CSRF tokens during POST requests including login, password changes, and user signup.
This ensures our application is protected against CSRF attacks as described in the [OWASP guidelines](https://owasp.org/www-community/attacks/csrf).

### Tests Included

Areas tested include:
- Login Form CSRF Protection
- Signup Form CSRF Protection
- Password Change CSRF Protection

Types of tests include:
- Rejection, missing token
- Acceptance with valid token
- Rejection with non-missing invalid token

### Test Implementation Details

Each CSRF test follows a two-step process:

1. **Token Retrieval**: First, a GET request is sent to the respective form page (`/login`, `/signup`, `/change_password`) to retrieve a page containing a CSRF token.
2. **Form Submission**: A POST request is then made with or without the retrieved CSRF token to test the form's response. This simulates user actions under normal and attack scenarios.

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

- **Adding Tests**: When adding new features, include comprehensive tests that cover both new functionalities and their integration into existing features (code writer or QA)
- **Existing Tests**: Ensure code modifications are backward compatible where possible and that they do not break existing tests (code writer)

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

The `utils.py` file contains functions for creating the fake database.
The `setup_fake_db.py` script is used to create a fake database instance and fill it with data.

### Tests Included

- **Fake Data Creation**: Confirms that users, organizations, locations, and hours can be created, added to sessions, and committed without issues.
- **Data Retrieval**: Tests retrieving users by their ID and asserts the correctness of the data like email format and user roles.
- **Data Validation**: Verifies the integrity of data relationships, ensuring that users are linked to valid organizations and all entities have expected attributes.
- **Authentication**: Tests to check authentication pathways including sign-up, login, logout, password changes, and password security.
- **Error Handling and Logging**: Log errors during data creation and handle exceptions with rollback.
- **Prevention of SQL Injections**: Tests for secure handling of safe and unsafe inputs within the fake database instance, preventing malicious actions such as returning all records or dropping tables.

### Additional Tests - in progress

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
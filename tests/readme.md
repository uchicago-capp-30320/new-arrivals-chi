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

## Writing Tests

Test files are organized by their respective application components.

## Database Operation Tests

The `db_test.py` file focuses on testing database operations and consistency across our application.

It utilizes fixtures for the app, logger, and database and ensures all tests run within the application context.

### Tests Included

- **Fake Data Creation**: Confirms that users, organizations, locations, and hours can be created, added to sessions, and committed without issues.
- **Data Retrieval**: Tests retrieving users by their ID and asserts the correctness of the data like email format and user roles.
- **Data Validation**: Verifies the integrity of data relationships, ensuring that users are linked to valid organizations and all entities have expected attributes.
- **Error Handling and Logging**: Log errors during data creation and handle exceptions with rollback.

### Additional Tests - in progress

Simple starter tests are defined in `app_home_test.py`, which contains functions to test specific aspects of the home page such as,
- `test_home_page_status`: Verifies that the home page loads correctly.
- `test_home_contains_welcome_message`: Checks for the presence of a welcome message on the home page.

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

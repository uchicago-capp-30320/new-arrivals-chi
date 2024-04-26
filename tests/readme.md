# Flask Application Testing Documentation

## Testing Framework

We utilize `pytest` along with the `pytest-flask` plugin to facilitate our testing.

### Configuration with `conftest.py`

The core configurations for our tests are managed through `conftest.py`, which includes fixtures for the Flask application and its test client.
The fixtures can be used across multiple test files.

#### Fixtures Provided

- `app`: Configures and provides the Flask application instance, testing enabled
- `client`: Provides a test client for the application

## Writing Tests

Test files are organized by their respective application components.
Tests are currently written to cover expected content and functionality, but "stress tests" will be added in the future.

### Example Test Setup

Tests are defined in files like `app_home_test.py`, which contains functions to test specific aspects of the home page:

- `test_home_page_status`: Verifies that the home page loads correctly.
- `test_home_contains_welcome_message`: Checks for the presence of a welcome message on the home page.
- Additional tests ensure functionality like language settings, navigation links, and interactive elements such as buttons.

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

Replace `test_home_page_status` with any specific test function you need to execute.

## Contributing

### Guidelines

- **Adding Tests**: When adding new features, include comprehensive tests that cover both new functionalities and their integration into existing features (code writer or QA)
- **Existing Tests**: Ensure code modifications are backward compatible where possible and that they do not break existing tests (code writer)

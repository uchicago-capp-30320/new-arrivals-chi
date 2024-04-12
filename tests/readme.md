# Pytest readme

To run tests:
all: `poetry run pytest`
specific test: `poetry run pytest tests/test_example.py::test_example`
where `test_example` is the name of the test function.

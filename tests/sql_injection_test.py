"""
Project: New Arrivals Chi
File name: sql_injection_test.py
Associated Files: new_arrivals_chi/app/main.py, new_arrivals_chi/app/logger_config.py, 
                  tests/db_test.py


This test suite performs testing on the database to ensure that input handling, 
particularly regarding SQL injections, is secure and prevents unauthorized database 
access or manipulation.


Methods:
    - test_safe_injections: Test function for testing safe input handling or prevention
                            of SQL injections.
    - test_unsafe_injections_return_all_rows: Test function for an unsafe input 
                                              attempting to return all rows from the
                                              database.
    - test_unsafe_injections_alter_table: Test function for an unsafe input attempting
                                          to alter the database table structure.
    - test_line_comments_injection: Test function for testing prevention of line comments
                                    in SQL queries.
    - test_union_injection: Test function for testing prevention of Union-based SQL injections.
    - test_unsafe_error_based_injection: Test function for testing error-based SQL injections 
                                         that find column names.
    - test_unsafe_boolean_based_blind_sql_injection: Test function for simulating an SQL 
                                                    injection attack using an IF statement.




Last updated:
@Author: Xiomara Salazar @xiomara0
@Date: 05/09/2024

Creation:
@Author: Xiomara Salazar @xiomara0
@Date: 05/09/2024
"""

from sqlalchemy import select
from .db_test import create_fake_user, create_fake_organization
from .setup_fake_db import main
from new_arrivals_chi.app.database import User
from new_arrivals_chi.app.main import create_app


# creating fake users for queries
test_org = create_fake_organization()
test_user = create_fake_user(test_org)


def database_query(setup_logger, input_value): 
    """
    Function to execute a database query and check the number of rows returned.

    Args:
    - setup_logger: Setup logger.
    - input_value: Input value for the database query that filters on email
    """
    test_app, test_db = main()

    logger = setup_logger("test_injections")

    try:
        with test_app.app_context():
            logger.info("Starting injection test")

            session = test_db.session
            logger.info("Attempting to retrieve user with test input")
            filtered_users_select = select(User).where(User.email == input_value)
            all_users_select = select(User)
            
            all_users = session.execute(all_users_select).scalars().all()
            filtered_users = session.execute(filtered_users_select).scalars().all()

            logger.info("SQL query was executed")

            assert bool(all_users), "No records found in the database."

            logger.info(f"There are records in the database.\n\
                        Found {len(all_users)} records.")
            
            metadata = test_db.metadata
            
            test_db.session.remove()
            test_db.drop_all()
            logger.info("Test database removed and test tables dropped.")
            
            return len(filtered_users), metadata
            
    except Exception as e:
        logger.error(f"Error in database query: {e}")
        raise  # Raise the exception to be caught at a higher level



def test_safe_injections(setup_logger):
    """
    Test function for testing safe input handling or prevention of SQL injections.

    Args:
    - setup_logger: Setup logger.
    - input_value: Input value for the database query that filters on email

    Return: Asserts that fake user isn't in test 'user' table.
    """
    input_value = f"'{test_user.email}'"

    row_count, metadata = database_query(setup_logger, input_value)

    assert row_count == 0


def test_unsafe_injection_return_all_rows(setup_logger):
    """
    Test function for an unsafe input attempting to return all rows.

    Args:
    - setup_logger: Setup logger.
    - input_value: Input value for the database query that filters on email
    """
    input_value = f"'{test_user.email}' OR 1=1;"

    row_count, metadata = database_query(setup_logger, input_value)

    assert row_count == 0


def test_unsafe_injection_alter_table(setup_logger):
    """
    Test function for an unsafe input attempting to alter the table.
    Checks if table still exists and if anything is returned.

    Args:
    - setup_logger: Setup logger.
    - input_value: Input value for the database query that filters on email
    """
    input_value = f"'{test_user.email}'; DROP TABLE users; --"
    row_count, metadata = database_query(setup_logger, input_value)

    # Check if the 'user' table exists in the database metadata
    table_exists = "users" in metadata.tables

    assert table_exists, "Table 'user' does not exist"
    assert row_count == 0


def test_unsafe_line_comments_injection(setup_logger):
    """
    Test function for testing prevention of line comments in SQL queries.

    Args:
    - setup_logger: Setup logger.
    - input_value: Input value for the database query that filters on email
    """
    input_value = f"'{test_user.email}'; DROP TABLE users /*"
    row_count, metadata = database_query(setup_logger, input_value)

    # Check if the 'user' table exists in the database metadata
    table_exists = "users" in metadata.tables

    assert table_exists, "Table 'user' does not exist"
    assert row_count == 0


def test_unsafe_union_injection(setup_logger):
    """
    Test function for testing prevention of Union-based SQL injections.

    Args:
    - setup_logger: Setup logger.
    - input_value: Input value for the database query that filters on email
    """
    input_value = f"{test_user.email} UNION SELECT * FROM organization;"

    row_count, metadata = database_query(setup_logger, input_value)

    assert row_count == 0


def test_unsafe_error_based_injection(setup_logger):
    """
    Test function for testing error-based SQL injections that find column names.

    Args:
    - setup_logger: Setup logger.
    - input_value: Input value for the database query that filters on email
    """
    input_value = f"'{test_user.email}' HAVING 1=1 UNION SELECT 1, \
                    group_concat(name) FROM sqlite_master WHERE type='table';"

    row_count, metadata = database_query(setup_logger, input_value)

    assert row_count == 0


def test_unsafe_if_statement(setup_logger):
    """
    Test function for simulating an SQL injection attack using an IF statement.

    Args:
    - setup_logger: Setup logger.
    - input_value: Input value for the database query that filters on email
    """
    input_value = (
        f"{test_user.email}' OR 1=1; IF 1=1 BEGIN SELECT 1 ELSE SELECT 0 END --"
    )

    row_count, metadata = database_query(setup_logger, input_value)

    assert row_count == 0, "SQL Injection with IF statement successful"
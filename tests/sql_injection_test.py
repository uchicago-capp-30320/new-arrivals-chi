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
    - test_unsafe_boolean_based_blind_sql_injection: [In progress] Test function for blind
                                                     sql injection. Need to think about true 
                                                     input more.



Last updated:
@Author: Xiomara Salazar @xiomara0
@Date: 05/07/2024

Creation:
@Author: Xiomara Salazar @xiomara0
@Date: 05/06/2024
"""

import pytest
from sqlalchemy.orm import Session
from sqlalchemy import select, inspect
from tests.db_test import create_fake_user, create_fake_organization
from new_arrivals_chi.app.database import User


test_org = create_fake_organization()
test_user = create_fake_user(test_org)


def database_query(app, database, setup_logger, input_value):
    """
    Function to execute a database query and check the number of rows returned.
    """

    logger = setup_logger("test_injections")

    with app.app_context():
        logger.info("Starting injection test")
    
        # Attempt to retrieve a user with the safe input value
        with Session(bind=database.engine) as session:
            logger.info("Attempting to retrieve user with test input")
            users_select = select(User).where(User.email == input_value)
            users = session.execute(users_select).scalars().all()
            
            return len(users)


def test_safe_injections(app, database, setup_logger): 
    """
    Test function for testing safe input handling or prevention of SQL injections.
    """

    input_value = f"'{test_user.email}'"

    row_count = database_query(app, database, setup_logger, input_value)

    assert row_count == 0 ## it's okay if this one is 0 right? since I am using dummy data
                          ## won't it always be 0; should i use real data for the other ones?


def test_unsafe_injection_return_all_rows(app, database, setup_logger): 
    """
    Test function for an unsafe input attempting to return all rows.
    """

    input_value = f"'{test_user.email}' OR 1=1;"

    row_count = database_query(app, database, setup_logger, input_value)

    assert row_count == 0 


def test_unsafe_injection_alter_table(app, database, setup_logger): 
    """
    Test function for an unsafe input attempting to alter the table.
    Checks if table still exists and if anything is returned.
    """

    input_value = f"'{test_user.email}'; DROP TABLE users; --"
    metadata = database.metadata

    if 'users' in metadata.tables:
        table_exists = True
    else:
        table_exists = False

    assert table_exists, "Table 'users' does not exist"

    row_count = database_query(app, database, setup_logger, input_value)

    assert row_count == 0


def test_unsafe_line_comments_injection(app, database, setup_logger): 
    """
    Test function for testing prevention of line comments in SQL queries.
    """

    input_value = f"'{test_user.email}'; DROP TABLE users /*"
    metadata = database.metadata

    if 'users' in metadata.tables:
        table_exists = True
    else:
        table_exists = False

    assert table_exists, "Table 'users' does not exist"

    row_count = database_query(app, database, setup_logger, input_value)

    assert row_count == 0


def test_unsafe_union_injection(app, database, setup_logger):
    """
    Test function for testing prevention of Union-based SQL injections.
    """

    input_value = f"{test_user.email} UNION SELECT * FROM organizations;"

    row_count = database_query(app, database, setup_logger, input_value)

    assert row_count == 0

def test_unsafe_error_based_injection(app, database, setup_logger):
    """
    Test function for testing error-based SQL injections that find column names.
    """

    input_value = f"'{test_user.email}' HAVING 1=1 UNION SELECT 1, \
                    group_concat(name) FROM sqlite_master WHERE type='table';"

    row_count = database_query(app, database, setup_logger, input_value)

    assert row_count == 0

def test_unsafe_boolean_based_blind_sql_injection(app, database, setup_logger):
    """
    [In progress] Test function for blind sql injection. Need to think
    about true input more
    """

    #input_value_true = f"'{test_user.email}' AND 1=1; --"
    input_value_false = f"'{test_user.email}'  AND 1=2; --"

    #row_count_true = database_query(app, database, setup_logger, input_value_true)
    row_count_false = database_query(app, database, setup_logger, input_value_false)

    #assert row_count_true > 0, "Boolean-Based Blind SQL Injection detected (True condition)"
    assert row_count_false == 0, "Boolean-Based Blind SQL Injection detected (False condition)"
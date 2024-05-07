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



Last updated:
@Author: Xiomara Salazar @xiomara0
@Date: 05/07/2024

Creation:
@Author: Xiomara Salazar @xiomara0
@Date: 05/06/2024
"""

import pytest
import sqlite3
from new_arrivals_chi.app.main import db
from new_arrivals_chi.app.logger_config import setup_logger
from tests.db_test import create_fake_user
from sqlalchemy.orm import Session
from sqlalchemy import select


@pytest.mark.usefixtures("database")
def db_connection(database):
    """
    Function to connect to a database. It uses fixture to get a created db
    instance.

    Input: Database, database from fixture
    """

    connection = database  
    yield connection  
    connection.close()  


def database_query(db_connection, input_value):
    """
    Function to execute a database query and check the number of rows returned.
    """
    
    cursor = db_connection.cursor()
    query = f"SELECT * FROM users {input_value} ;"

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        print("Query executed successfully. Results:")
        return len(rows)

    except sqlite3.Error as e:
        print("Error executing query:", e)
        return -1


def test_safe_injections(database_query): 
    """
    Test function for testing safe input handling or prevention of SQL injections.
    """

    test_user = create_fake_user()
    input_value = f"WHERE email = '{test_user.email}'"

    row_count = database_query(db_connection, input_value)

    assert row_count == 0 ## it's okay if this one is 0 right?


def test_unsafe_injection_return_all_rows(db_connection): 
    """
    Test function for an unsafe input attempting to return all rows.
    """

    test_user = create_fake_user()
    input_value = f"WHERE email = '{test_user.email}' OR 1=1;"

    row_count = database_query(db_connection, input_value)

    assert row_count == 0 


def test_unsafe_injection_alter_table(db_connection): 
    """
    Test function for an unsafe input attempting to alter the table.
    """

    alter_table_input = "'; DROP TABLE users; --"

    row_count = database_query(db_connection, alter_table_input)

    assert row_count == 0 


def test_unsafe_line_comments_injection(db_connection): 
    """
    Test function for testing prevention of line comments in SQL queries.
    """

    test_user = create_fake_user()
    input_value = f"id = {test_user.id}; -- This is a line comment"

    row_count = database_query(db_connection, input_value)

    assert row_count == 0


def test_unsafe_union_injection(db_connection): 
    """
    Test function for testing prevention of Union-based SQL injections.
    """

    test_user = create_fake_user()
    input_value = f"id = {test_user.id} UNION SELECT * FROM organizations;"

    row_count = database_query(db_connection, input_value)

    assert row_count == 0

def test_unsafe_error_based_injection(db_connection): 
    """
    Test function for testing error-based SQL injections that find column names.
    """

    test_user = create_fake_user()
    input_value = f"password = '{test_user.password}' HAVING 1=1 UNION SELECT 1, \
                    group_concat(name) FROM sqlite_master WHERE type='table';"

    row_count = database_query(db_connection, input_value)

    assert row_count == 0

def test_unsafe_boolean_based_blind_sql_injection(db_connection):
    """
    Test function fo testing blind sql injection.
    """
    test_user = create_fake_user()

    input_value_true = f"email = {test_user.email} AND 1=1; --"
    input_value_false = f"name = {test_user.email}  AND 1=2; --"

    row_count_true = database_query(db_connection, input_value_true)
    row_count_false = database_query(db_connection, input_value_false)

    assert row_count_true > 0, "Boolean-Based Blind SQL Injection detected (True condition)"
    assert row_count_false == 0, "Boolean-Based Blind SQL Injection detected (False condition)"
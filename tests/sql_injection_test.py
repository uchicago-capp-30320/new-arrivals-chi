"""
Project: New Arrivals Chi
File name: sql_injection_test.py
Associated Files:


This test suite performs testing on the database to 

Methods:

Last updated:
@Author: Xiomara Salazar @xiomara0
@Date: 05/06/2024

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


def test_safe_injections(test_database_query): 
    """
    Test function for testing safe input handling or prevention of SQL injections.
    """
    test_user = create_fake_user()
    email_filter = f"WHERE email = '{test_user.email}'"

    row_count = database_query(db_connection, email_filter)

    assert row_count == 0 ## it's okay if this one is 0 right?


# Test for unsafe input handling or prevention of SQL injections
def test_unsafe_injection_return_all_rows(db_connection): 
    """
    Test function for an unsafe input attempting to return all rows.
    """
    return_all_rows_input = "name = 'Alice' OR 1=1;"

    row_count = database_query(db_connection, return_all_rows_input)
    assert row_count == 0 


def test_unsafe_injection_alter_table(db_connection): 
    """
    Test function for an unsafe input attempting to alter the table.
    """
    
    alter_table_input = "'; DROP TABLE users; --"

    row_count = database_query(db_connection, alter_table_input)
    assert row_count == 0 




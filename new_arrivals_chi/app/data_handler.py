"""Project: new_arrivals_chi.

File name: data_handler.py
Associated Files:
   authorize_routes.py.

This file contains utility methods for validating user input and handling d
atabase operations.

Methods:
    * create_user - Creates a new user in the database.
    * change_db_password - Changes the password for the current user in the
      database.

Creation:
@Author: Madeleine Roberts @MadeleineKRoberts
@Date: 05/09/2024
"""

from new_arrivals_chi.app.database import db, User
from flask_login import current_user
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def create_user(email, password):
    """Creates a new user in the database.

    Parameters:
        email (str): The email address of the new user.
        password (str): The password of the new user.

    Returns:
        User: The newly created User object.
    """
    new_user = User(
        email = email,
        password = bcrypt.generate_password_hash(password).decode('utf-8'),
    )
    db.session.add(new_user)
    db.session.commit()

    return new_user


def change_db_password(password):
    """Changes the password for the current user in the database.

    Parameters:
        password (str): The new password for the current user.
    """
    current_user.password = bcrypt.generate_password_hash(password).decode('utf-8')
    db.session.commit()

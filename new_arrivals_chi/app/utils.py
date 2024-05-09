"""Project: new_arrivals_chi.

File name: utils.py
Associated Files:
   authorize_routes.py.

This file contains utility methods for validating user input.


Methods:
    * validate_email_syntax — Validates the syntax of an email address.
    * validate_password - Validates the strength of a password.

Creation:
@Author: Madeleine Roberts @MadeleineKRoberts
@Date: 04/19/2024
"""


import re
import os
import logging
from datetime import datetime
from new_arrivals_chi.app.database import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from password_strength import PasswordPolicy, PasswordStats

def extract_signup_data(form):
    email = form.get("email").lower()
    password = form.get("password")
    password_confirm = form.get("password_confirm")
    return email, password, password_confirm

# Reference: https://docs.kickbox.com/docs/python-validate-an-email-address
def validate_email_syntax(email):
    """Validates the syntax of an email address.

    This function checks if the provided email address follows the standard
    syntax rules for email addresses.

    Parameters:
        email (str): The email address to be validated.

    Returns:
        bool: True if the email syntax is valid, False otherwise.
    """
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


# Reference: https://pypi.org/project/password-strength/#passwordstats
def validate_password(password):
    """Validates the strength of a password.

    This function checks if the provided password meets the strength
    requirements.The password must be at least 8 characters long and contain at
    least one lowercase letter, one uppercase letter, one digit, and one special
    character. Additionally, the password should not contain any whitespace
    characters.

    Parameters:
        password (str): The password to be validated.

    Returns:
        bool: True if the password meets the strength requirements,
        False otherwise.
    """
    
    policy = PasswordPolicy.from_names(
        length=8,
        uppercase=1,  # need min. 1 uppercase letter
        numbers=1,  # need min. 1 digit
        special=1,  # need min. 1 special character
        strength=0.5
    )
    
    policy_reqs = len(policy.test(password))
    print(policy.password(password).strength())

    no_space = re.search(r"\s", password) is None

    return policy_reqs==0 and no_space
   

def create_user(email, password):
    new_user = User(
        email=email,
        password=generate_password_hash(password, method="pbkdf2:sha256"),
    )
    db.session.add(new_user)
    db.session.commit()

    return new_user


def setup_logger(name):
    """Create a logger for recording the output of the script."""
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"{name}_{timestamp}.log"
    log_path = os.path.join(log_directory, log_filename)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

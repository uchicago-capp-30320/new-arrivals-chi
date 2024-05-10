"""Project: new_arrivals_chi.

File name: utils.py
Associated Files:
   authorize_routes.py.

This file contains utility methods for validating user input.

Methods:
    * validate_email_syntax — Validates the syntax of an email address.
    * validate_password - Validates the strength of a password.
    * extract_signup_data - Extracts signup data from a request object.
    * extract_new_pw_data - Extracts new password data from a request object.
    * setup_logger - Creates a logger for recording the output of the script.

Last Updated:
@Author: Madeleine Roberts @MadeleineKRoberts
@Date: 05/19/2024

Creation:
@Author: Madeleine Roberts @MadeleineKRoberts
@Date: 04/19/2024
"""


import re
import os
import logging
from datetime import datetime
from password_strength import PasswordPolicy


def extract_signup_data(form):
    """Extracts signup data from a POST request form.

    Parameters:
        form (ImmutableMultiDict): The ImmutableMultiDict object containing
            form data from a POST request.
            It should have keys "email", "password", and "password_confirm".

    Returns:
        tuple: A tuple containing the extracted email, password, and
            password_confirm.
    """
    email = form.get("email").lower()
    password = form.get("password")
    password_confirm = form.get("password_confirm")
    return email, password, password_confirm


def extract_new_pw_data(form):
    """Extracts new password data from a POST request form.

    Parameters:
        form (ImmutableMultiDict): The ImmutableMultiDict object containing
            form data from a POST request. It should have keys "old_password",
            "new_password", and "new_password_confirm".

    Returns:
        tuple: A tuple containing the extracted old_password, new_password,
        and new_password_confirm.
    """
    old_password = form.get("old_password")
    new_password = form.get("new_password")
    new_password_confirm = form.get("new_password_confirm")
    return old_password, new_password, new_password_confirm


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
        strength=0.66,  # Minimum value to be considered a strong password
    )

    policy_reqs = len(policy.test(password))
    print(policy.password(password).strength())

    no_space = re.search(r"\s", password) is None

    return policy_reqs == 0 and no_space


def setup_logger(name):
    """Create a logger for recording the output of the script.

    Parameters:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The configured logger object.
    """
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

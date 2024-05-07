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


# Reference: ChatGPT supported regex
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
    # 1+ lower case, 1+ upper case, 1+ number, 1+ special characters
    pattern = r"(?=.*[a-z]+)(?=.*[A-Z]+)(?=.*\d+)(?=.*[\W_]+).+"
    valid_characters = re.fullmatch(pattern, password) is not None

    no_space = re.search(r"\s", password) is None

    return len(password) >= 8 and valid_characters and no_space

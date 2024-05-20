"""Project: new_arrivals_chi.

File name: utils.py
Associated Files:
   authorize_routes.py.

This file contains utility methods for validating user input.

Methods:
    * extract_signup_data - Extracts signup data from a request object.
    * extract_new_pw_data - Extracts new password data from a request object.
    * validate_email_syntax — Validates the syntax of an email address.
    * validate_password - Validates the strength of a password.
    * verify_password - Verifies a candidate password against a hashed password.
    * setup_logger - Creates a logger for recording the output of the script.

Last Updated:
@Author: Madeleine Roberts @MadeleineKRoberts
@Date: 05/19/2024

Creation:
@Author: Madeleine Roberts @MadeleineKRoberts
@Date: 04/19/2024
"""

import logging
import json
import re
import os
import bleach
import us
from datetime import datetime
from password_strength import PasswordPolicy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


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


def extract_registration_info(form):
    """
    """
    location = {
        'street' : bleach.clean(form.get("street")),
        'city' : validate_city(bleach.clean(form.get("city"))),
        'state' : validate_state(bleach.clean(form.get("state"))),
        'zip' : validate_zip_code(bleach.clean(form.get("zip-code"))),
    }

    hours = {
        '1': extract_hours(form, 'monday'),
        '2': extract_hours(form, 'tuesday'),
        '3': extract_hours(form, 'wednesday'),
        '4': extract_hours(form, 'thursday'),
        '5': extract_hours(form, 'friday'),
        '6': extract_hours(form, 'saturday'),
        '7': extract_hours(form, 'sunday')
    }

    print(hours)

    return location, hours

def extract_hours(form, day):
    hours_list = []
    prev_close = None

    # Calculate the count of hour entries for the specified day
    count = sum(1 for key in form.keys() if key.startswith(f'{day}-open-'))

    # Process each hour entry
    for curr_hour in range(1, count + 1):
        open_time = form.get(f'{day}-open-{curr_hour}')
        close_time = form.get(f'{day}-close-{curr_hour}')
        
        # Validate the hours
        if open_time and close_time:
            valid_hours = validate_hours(open_time, close_time, prev_close)

            if valid_hours is None:
                # If an invalid entry is found, return None
                return None
            
            hours_list.append(valid_hours)
            # Update prev_close with the new close time
            _, new_close = valid_hours
            prev_close = new_close

    return hours_list

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
    if len(password) < 8:
        return False

    policy = PasswordPolicy.from_names(
        length=8,
        uppercase=1,  # need min. 1 uppercase letter
        numbers=1,  # need min. 1 digit
        special=1,  # need min. 1 special character
        strength=0.66,  # Minimum value to be considered a strong password
    )

    policy_reqs = len(policy.test(password))

    no_space = re.search(r"\s", password) is None

    return policy_reqs == 0 and no_space


def verify_password(pw_hash, candidate):
    """Verifies a candidate password against a hashed password.

    This function compares a candidate password against a hashed password
    to check if they match.

    Parameters:
        pw_hash (str): The hashed password.
        candidate (str): The candidate password to be verified.

    Returns:
        bool: True if the candidate password matches the hashed password,
        False otherwise.
    """
    return bcrypt.check_password_hash(pw_hash, candidate)


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

def load_translations():
    """Loads translations from JSON files for supported languages.

    Returns:
        dict: A dictionary containing translations for supported languages.
    """
    languages = ["en", "es"]
    translations = {}
    for lang in languages:
        with open(f"new_arrivals_chi/app/languages/{lang}.json", "r") as file:
            translations[lang] = json.load(file)
    return translations

def validate_city(city):
    pattern = re.compile(r"^[a-zA-Z]+(?:[\s-'][a-zA-Z]+)*$")
   
    if city is not None or not bool(pattern.match(city)):
        return None
    return city

def validate_state(state_code):
    if state_code is None or us.states.lookup(state_code) is None:
        return None
    return state_code


def validate_zip_code(zip_code):
    pattern = re.compile(r'^\d{5}(?:-\d{4})?$')

    if zip_code is None or not bool(pattern.match(zip_code)):
        return None
    return zip_code


def validate_hours(open_time, close_time, prev_close):
    # Clean the input times
    open_cleaned = bleach.clean(open_time)
    close_cleaned = bleach.clean(close_time)

    # Validate the times
    if (prev_close is None or open_cleaned > prev_close) and open_cleaned < close_cleaned:
        return open_cleaned, close_cleaned

    return None




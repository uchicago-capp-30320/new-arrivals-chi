"""Project: new_arrivals_chi.

File name: utils.py
Associated Files:
   authorize_routes.py.

This file contains utility methods for validating user input.

Methods:
    * extract_signup_data - Extracts signup data from a request object.
    * extract_new_pw_data - Extracts new password data from a request object.
    * extract_registration_info - Extracts and validates registration
        information from a form.
    * extract_hours - Extracts and validates operating hours for a specific day
        from a form.
    * validate_email_syntax — Validates the syntax of an email address.
    * validate_password - Validates the strength of a password.
    * verify_password - Verifies a candidate password against a hashed password.
    * validate_street - Validates the street address format.
    * validate_city - Validates the city name.
    * validate_state - Validates the state code.
    * validate_zip_code - Validates the ZIP code format.
    * load_neighborhoods - Loads neighborhood values from a file.
    * validate_neighborhood - Validates the neighborhood name.
    * validate_hours - Validates the operating hours.
    * setup_logger - Creates a logger for recording the output of the script.
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
from new_arrivals_chi.app.constants import LANGUAGES

from flask import current_app


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
    """Extracts and validates registration information from a form.

    This function retrieves location and hours information from a form,
    validates each field, and returns the validated data.

    Parameters:
        form (dict): A dictionary containing form data with keys for street,
                     city, state, zip-code, neighborhood, and operating hours
                     for each day of the week.

    Returns:
        tuple: A tuple containing two dictionaries:
               - location (dict): The validated location information with keys
                 'street', 'city', 'state', 'zip-code', and 'neighborhood'.
               - hours (dict): The validated operating hours for each day of
                 the week, with keys as day numbers (1 for Monday, 2 for
                 Tuesday, etc.) and values as lists of tuples with opening and
                 closing times.
    """
    location = {
        "street": validate_street(bleach.clean(form.get("street"))),
        "city": validate_city(bleach.clean(form.get("city"))),
        "state": validate_state(bleach.clean(form.get("state"))),
        "zip-code": validate_zip_code(bleach.clean(form.get("zip-code"))),
        "neighborhood": validate_neighborhood(
            bleach.clean(form.get("neighborhood"))
        ),
    }

    hours = {
        "1": extract_hours(form, "monday"),
        "2": extract_hours(form, "tuesday"),
        "3": extract_hours(form, "wednesday"),
        "4": extract_hours(form, "thursday"),
        "5": extract_hours(form, "friday"),
        "6": extract_hours(form, "saturday"),
        "7": extract_hours(form, "sunday"),
    }

    return location, hours


def extract_hours(form, day):
    """Extracts and validates operating hours for a specific day from a form.

    This function retrieves operating hours entries for a specified day,
    validates each entry, and returns a list of validated hours.

    Parameters:
        form (dict): A dictionary containing form data with keys for opening
                     and closing times for each day of the week.
        day (int): The day of the week for which to extract hours.

    Returns:
        list: A list of tuples containing validated opening and closing times
              for the specified day, or None if validation fails.
    """
    hours_list = []
    prev_close = None

    # Calculate the count of hour entries for the specified day
    count = sum(1 for key in form.keys() if key.startswith(f"{day}-open-"))

    # Process each hour entry
    for curr_hour in range(1, count + 1):
        open_time = form.get(f"{day}-open-{curr_hour}")
        close_time = form.get(f"{day}-close-{curr_hour}")

        # Validate the hours
        if open_time and close_time:
            valid_hours = validate_hours(open_time, close_time, prev_close)

            if valid_hours is None:
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
        strength=0.4,
    )

    policy_reqs = len(policy.test(password))

    no_space = re.search(r"\s", password) is None

    return policy_reqs == 0 and no_space


def validate_phone_number(phone_number):
    """Validates the format of a phone number.

    This function checks if the provided phone number is in a valid format.
    The phone number is in the format "###-###-####", where each "#" represents
    a digit.

    Parameters:
        phone_number (str): The phone number to be validated.

    Returns:
        bool: True if the phone number is in a valid format, False otherwise.
    """
    does_match = re.match(r"^\d{3}-\d{3}-\d{4}$", phone_number)

    return does_match is not None


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


def load_translations():
    """Loads translations from JSON files for supported languages.

    Returns:
        dict: A dictionary containing translations for supported languages.
    """
    translations = {}
    for lang in LANGUAGES:
        with open(f"new_arrivals_chi/app/languages/{lang}.json", "r") as file:
            translations[lang] = json.load(file)
    return translations


def validate_street(street):
    """Validates the street address format.

    This function checks if the given street address matches the expected
    pattern, which includes alphanumeric characters, spaces, commas,
    hyphens, periods, and hash symbols.

    Parameters:
        street (str): The street address to validate.

    Returns:
        str: The validated street address if valid, None otherwise.
    """
    pattern = re.compile(r"^[0-9a-zA-Z\s,'-\.#]+$")

    if street is None or not bool(pattern.match(street)):
        return None
    return street


def validate_city(city):
    """Validates the city name.

    This function checks if the given city name matches the expected pattern
    and is constrained to "Chicago" for the first iteration.

    Parameters:
        city (str): The city name to validate.

    Returns:
        str: The validated city name if valid, None otherwise.
    """
    pattern = re.compile(r"^[a-zA-Z]+(?:[\s\-'][a-zA-Z]+)*$")

    # Contrained to Illinois for the first iteration
    if city is None or not bool(pattern.match(city)) or city != "Chicago":
        return None
    return city


def validate_state(state_code):
    """Validates the state code.

    This function checks if the given state code is valid and is constrained to
    "IL" (Illinois) for the first iteration.

    Parameters:
        state_code (str): The state code to validate.

    Returns:
        str: The validated state code if valid, None otherwise.
    """
    # Contrained to Illinois for the first iteration
    if (
        state_code is None
        or us.states.lookup(state_code) is None
        or state_code != "IL"
    ):
        return None
    return state_code


def validate_zip_code(zip_code):
    """Validates the ZIP code format.

    This function checks if the given ZIP code matches the expected pattern.

    Parameters:
        zip_code (str): The ZIP code to validate.

    Returns:
        str: The validated ZIP code if valid, None otherwise.
    """
    pattern = re.compile(r"^\d{5}(?:-\d{4})?$")

    if zip_code is None or not bool(pattern.match(zip_code)):
        return None
    return zip_code


def load_neighborhoods():
    """Loads Chicago neighborhood values from a file in static folder.

    This function reads neighborhood values from a specified text file and
    returns them as a list.

    Returns:
        list: A list of neighborhood values.
    """
    with open(
        "new_arrivals_chi/app/static/neighborhood_values.txt", "r"
    ) as file:
        return file.read().splitlines()


def validate_neighborhood(neighborhood):
    """Validates the neighborhood name.

    This function checks if the given neighborhood name matches the expected
    pattern and is a valid neighborhood in Chicago as defined in the
    configuration.

    Parameters:
        neighborhood (str): The neighborhood name to validate.

    Returns:
        str: The validated neighborhood name if valid, None otherwise.
    """
    # Constrained to Chicago neighborhoods for the first iteration
    chicago_neighborhood = neighborhood in current_app.config["NEIGHBORHOODS"]

    pattern = re.compile(r"^[A-Za-z_]+$")

    if (
        neighborhood is None
        or not bool(pattern.match(neighborhood))
        or not chicago_neighborhood
    ):
        return None
    return neighborhood


def validate_hours(open_time, close_time, prev_close):
    """Validates the operating hours.

    This function cleans and validates the given opening and closing times,
    ensuring that the opening time is earlier than the closing time and later
    than the previous closing time if provided.

    Parameters:
        open_time (str): The opening time in HH:MM format.
        close_time (str): The closing time in HH:MM format.
        prev_close (str): The previous closing time in HH:MM format, if any.

    Returns:
        tuple: A tuple containing the validated opening and closing times if
               valid, None otherwise.
    """
    # Clean the input times
    open_cleaned = bleach.clean(open_time)
    close_cleaned = bleach.clean(close_time)

    # Validate the times
    if (
        prev_close is None or open_cleaned > prev_close
    ) and open_cleaned < close_cleaned:
        return open_cleaned, close_cleaned

    return None


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


def create_temp_pwd(email, phone):
    """Creates a temporary password for a new user.

    This function generates a temporary password for a new user based using the
    first part of the email address and the first three digits of the provided
    phone number.
    Parameters:
        email (str): The email address of the new user.
        phone (str): The phone number of the new user.

    Returns:
        str: The temporary password generated for the new user.
    """
    email_string = email.split("@")[0]
    phone_digits = phone[0:3]

    temp_pwd = email_string + phone_digits

    return temp_pwd

"""
This module contains functions for validating data and generating fake data.

Dependencies:
    - random
    - re
    - app.models.users

Functions:
    - is_valid_email(email): check if the given email address is valid.
    - is_valid_phone_number(phone_number): validates whether a phone number is in a valid format.
    - is_free_username(username, _id): check if the given username is free.
    - is_free_email(email, _id): check if the given email address is free.    
    - is_free_phone_number(phone_number, _id): validates whether a phone number is free.
    - is_valid_date(date): validates whether a date is in a valid format.
    - fake_phone_number(): generate a random phone number in format "+{1,2,3}xxxxxxxxxx".

"""

import random
import re

from app.models.users import User


def is_valid_email(email) -> bool:
    """
    Check if the given email address is valid.

    Args:
        - email (str): The email address to validate.

    Returns:
        - bool: True if the email address is valid, False otherwise.

    """

    # regular expression for email validation
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # use the regular expression to match the email address
    match = re.match(pattern, email)

    return match is not None


def is_valid_phone_number(phone_number) -> bool:
    """
    Validates whether a phone number is in a valid format.

    Args:
        - phone_number (str): The phone number to validate.

    Returns:
        - bool: True if the phone number is valid, False otherwise.

    """

    # Regular expression for matching phone number in format "+{1,2,3}xxxxxxxxxx"
    regex = r"^\+[1,3]\d{11}$"
    return re.match(regex, phone_number) is not None


def is_free_username(username, _id) -> bool:
    """
    Check if the given username is free.

    Args:
        - username (str): The username to validate.

    Returns:
        - bool: True if the username is free, False otherwise.

    """

    return (
        User.query.filter_by(username=username).filter(User.id != _id).first() is None
    )


def is_free_email(email, _id) -> bool:
    """
    Check if the given email address is free.

    Args:
        - email (str): The email address to validate.

    Returns:
        - bool: True if the email address is free, False otherwise.

    """

    return User.query.filter_by(email=email).filter(User.id != _id).first() is None


def is_free_phone_number(phone_number, _id) -> bool:
    """
    Check if the given phone number is free.

    Args:
        - phone_number (str): The phone number to validate.

    Returns:
        - bool: True if the phone number is free, False otherwise.

    """

    return (
        User.query.filter_by(phone=phone_number).filter(User.id != _id).first() is None
    )


def is_valid_date(date) -> bool:
    """
    Validates whether a date is in a valid format.

    Args:
        - date (str): The date to validate.

    Returns:
        - bool: True if the date is valid, False otherwise.

    """

    # Regular expression for matching date in format "yyyy-mm-dd"
    regex = r"^\d{4}-\d{2}-\d{2}$"
    return re.match(regex, date) is not None


def fake_phone_number() -> str:
    """
    Generate a random phone number in format "+{1,2,3}xxxxxxxxxx".

    Returns:
        - str: The generated phone number.

    """

    country_code = random.choice([1, 3])
    number = "".join([str(random.randint(0, 9)) for _ in range(11)])
    phone_number = f"+{country_code}{number}"
    return phone_number

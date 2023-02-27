import re


def is_valid_email(email):
    """
    Check if the given email address is valid.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email address is valid, False otherwise.
    """

    # regular expression for email validation
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # use the regular expression to match the email address
    match = re.match(pattern, email)

    return match is not None


def is_valid_phone_number(phone_number):
    """
    Validates whether a phone number is in a valid format.

    Args:
        phone_number (str): The phone number to validate.

    Returns:
        bool: True if the phone number is valid, False otherwise.
    """

    # Regular expression for matching phone number in format "+{1,2,3}xxxxxxxxxx"
    regex = r"^\+[1,3]\d{11}$"
    return re.match(regex, phone_number) is not None

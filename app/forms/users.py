"""
This module contains the forms for the users blueprint. Forms are used to validate and sanitize
input from the user. The forms are defined using the Flask-WTF extension.

Dependencies:
    - flask_wtf
    - wtforms
    - wtforms.validators
    - app.forms.base
    - app.utils.validation

Exported classes:
    - SearchForm
    - UserForm

"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Optional, ValidationError

from app.forms.base import BaseSearchForm
from app.utils.validation import (
    is_free_email,
    is_free_phone_number,
    is_free_username,
    is_valid_date,
    is_valid_email,
    is_valid_phone_number,
)


class SearchForm(BaseSearchForm):
    """
    A form for search with optional fields. This class extends the `BaseSearchForm` class
    to add an optional `birth_date` field for filtering search results by birth date.

    Attributes:
        - search (StringField): The search field for filtering search results.
        - date_created (StringField): The date created field for filtering search results
        by creation date.
        - date_modified (StringField): The date modified field for filtering search results
        by modification date.
        - birth_date (StringField): The birth date field for filtering search results by birth date.

    """

    birth_date = StringField(validators=[Optional()])


class UserForm(FlaskForm):
    """
    This class is a subclass of the Flask-WTF FlaskForm class. It is used to validate and sanitize
    input from the user when searching for users.

    Attributes:
        - username (str): The username of the user.
        - email (str): The email of the user.
        - phone (str): The phone number of the user.
        - first_name (str): The first name of the user.
        - last_name (str): The last name of the user.
        - birth_date (str): The birth date of the user.
        - date_created (str): The date the user was created.
        - date_modified (str): The date the user was last modified.

    Methods:
        - validate_username: Validates the username.
        - validate_email: Validates the email.
        - validate_phone: Validates the phone number.
        - validate_birth_date: Validates the birth date.

    """

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    phone = StringField("Phone", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    birth_date = StringField("Birth Date", validators=[DataRequired()])
    date_created = StringField("Date Created", validators=[Optional()])
    date_modified = StringField("Date Modified", validators=[Optional()])

    def __init__(self, *args, **kwargs):
        """
        This method is the constructor for the UserForm class. It initializes the _id attribute
        and calls the constructor of the superclass.

        Parameters:
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

        """

        self._id = kwargs.pop("_id", True)
        super().__init__(*args, **kwargs)

    def validate_username(self, username):
        """
        This method validates the username.

        Parameters:
            - username (str): The username of the user.

        """

        if is_free_username(username.data, self._id) is False:
            raise ValidationError("Username is not free.")

    def validate_email(self, email):
        """
        This method validates the email.

        Parameters:
            - email (str): The email of the user.

        """

        if is_valid_email(email.data) is False:
            raise ValidationError("Email is not valid.")
        if is_free_email(email.data, self._id) is False:
            raise ValidationError("Email is not free.")

    def validate_phone(self, phone):
        """
        This method validates the phone number.

        Parameters:
            - phone (str): The phone number of the user.

        """

        if is_valid_phone_number(phone.data) is False:
            raise ValidationError("Phone is not valid.")
        if is_free_phone_number(phone.data, self._id) is False:
            raise ValidationError("Phone is not free.")

    def validate_birth_date(self, birth_date):
        """
        This method validates the birth date.

        Parameters:
            - birth_date (str): The birth date of the user.

        """

        if is_valid_date(birth_date.data) is False:
            raise ValidationError("Birth date is not valid.")

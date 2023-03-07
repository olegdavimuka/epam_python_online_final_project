"""
This module contains the forms for the purses blueprint. Forms are used to validate and sanitize
input from the user when searching for purses. The forms are defined using the Flask-WTF extension.

Dependencies:
    - flask_wtf
    - wtforms
    - wtforms.validators
    - app.forms.base

Exported classes:
    - SearchForm
    - PurseForm

"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Optional

from app.forms.base import BaseSearchForm


class SearchForm(BaseSearchForm):
    """
    A form for search with optional fields. This class extends the `BaseSearchForm` class
    to add an optional `user_id` and `currency` fields for filtering search results.

    Attributes:
        - search (StringField): The search field for filtering search results.
        - date_created (StringField): The date created field for filtering search results
        by creation date.
        - date_modified (StringField): The date modified field for filtering search results
        by modification date.
        - user_id (StringField): The user id field for filtering search results by user id.
        - currency (StringField): The currency field for filtering search results by currency.

    """

    user_id = StringField(validators=[Optional()])
    currency = StringField(validators=[Optional()])


class PurseForm(FlaskForm):
    """
    This class is a subclass of the Flask-WTF FlaskForm class. It is used to validate and sanitize
    input from the user when searching for purses.

    Attributes:
        - user_id (StringField): The user id field for filtering search results by user id.
        - currency (StringField): The currency field for filtering search results by currency.
        - balance (StringField): The balance field for filtering search results by balance.
        - date_created (StringField): The date created field for filtering search results
        by creation date.
        - date_modified (StringField): The date modified field for filtering search results
        by modification date.

    """

    user_id = StringField("User ID", validators=[Optional()])
    currency = StringField("Currency", validators=[Optional()])
    balance = StringField("Balance", validators=[Optional()])
    date_created = StringField("Date Created", validators=[Optional()])
    date_modified = StringField("Date Modified", validators=[Optional()])

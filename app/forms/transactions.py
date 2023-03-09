"""
This module contains the forms for the transactions blueprint. Forms are used to validate and
sanitize input from the user. The forms are defined using the Flask-WTF extension.

Dependencies:
    - flask_wtf
    - wtforms
    - wtforms.validators
    - app.forms.base
    - app.models.purses

Exported classes:
    - SearchForm
    - TransactionForm

"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Optional

from app.forms.base import BaseSearchForm
from app.models.purses import Purse


class SearchForm(BaseSearchForm):
    """
    A form for search with optional fields. This class extends the `BaseSearchForm` class
    to add an optional `purse_from_id`, `purse_to_id`, `purse_from_currency`, and
    `purse_to_currency` fields for filtering search results.

    Attributes:
        - search (StringField): The search field for filtering search results.
        - date_created (StringField): The date created field for filtering search results
        by creation date.
        - date_modified (StringField): The date modified field for filtering search results
        by modification date.
        - purse_from_id (StringField): The purse from id field for filtering search results
        by purse from id.
        - purse_to_id (StringField): The purse to id field for filtering search results
        by purse to id.
        - purse_from_currency (StringField): The purse from currency field for filtering search'
        results by purse from currency.
        - purse_to_currency (StringField): The purse to currency field for filtering search results
        by purse to currency.

    """

    purse_from_id = StringField(validators=[Optional()])
    purse_to_id = StringField(validators=[Optional()])
    purse_from_currency = StringField(validators=[Optional()])
    purse_to_currency = StringField(validators=[Optional()])


class TransactionForm(FlaskForm):
    """
    This class is a subclass of the Flask-WTF FlaskForm class. It is used to validate and sanitize
    input from the user when searching for transactions.

    Attributes:
        - purse_from_id (StringField): The purse from id field for filtering search results
        by purse from id.
        - purse_to_id (StringField): The purse to id field for filtering search results
        by purse to id.
        - purse_from_currency (StringField): The purse from currency field for filtering search
        results by purse from currency.
        - purse_to_currency (StringField): The purse to currency field for filtering search results
        by purse to currency.
        - purse_from_amount (StringField): The purse from amount field for filtering search results
        by purse from amount.
        - purse_to_amount (StringField): The purse to amount field for filtering search results
        by purse to amount.
        - date_created (StringField): The date created field for filtering search results

    """

    purse_from_id = StringField("Purse from id")
    purse_to_id = StringField("Purse to id")
    purse_from_amount = StringField("Purse from amount", validators=[DataRequired()])
    purse_to_amount = StringField("Purse to amount")
    date_created = StringField("Date created")

    def validate(self, extra_validators=None):
        """
        Validates the form. This method overrides the `validate` method of the FlaskForm class.

        Returns:
            - valid (bool): True if the form is valid, False otherwise.

        """

        valid = super().validate()
        if not valid:
            return False

        if self.purse_from_id.data == self.purse_to_id.data:
            self.purse_from_id.errors.append(
                "Purse from id and purse to id cannot be the same."
            )
            return False

        if Purse.query.get(self.purse_from_id.data).balance < float(
            self.purse_from_amount.data
        ):
            self.purse_from_id.errors.append(
                "Purse from id does not have enough balance."
            )
            return False

        return True

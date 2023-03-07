"""
This module defines the Purse class which represents a Purse entity in the database.
It also contains functions for converting date and time objects to string representations.

Dependencies:
    - logging
    - datetime
    - app.db
    - app.constants.currency
    - app.models.users

Exported classes:
    - Purse

"""

import logging
from datetime import datetime

from app import db
from app.constants.currency import Currency
from app.models.users import User


class Purse(db.Model):
    """
    A model that represents a user's purse in the financial system.

    Attributes:
        - __tablename__ (str): The name of the database table for this model.
        - id (int): The unique identifier of the purse.
        - user_id (int): The ID of the user who owns the purse.
        - currency (Currency): The currency type of the purse.
        - balance (float): The current balance of the purse.
        - date_created (datetime): The date and time when the purse was created.
        - date_modified (datetime): The date and time when the purse was last modified.
        - is_active (bool): A flag indicating whether the purse is active.
        - transactions_from (list): A list of transactions where the purse is the sender.
        - transactions_to (list): A list of transactions where the purse is the recipient.

    Methods:
        - __init__(self, **kwargs): Initializes a new purse instance.
        - __repr__(self): Returns a string representation of the purse.
        - date_created_str(self): Converts the date_created attribute to a string.
        - date_modified_str(self): Converts the date_modified attribute to a string.
        - to_dict(self): Returns a dictionary representation of the purse.

    """

    __tablename__ = "purses"
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    currency = db.Column(db.Enum(Currency), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_modified = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    is_active = db.Column(db.Boolean, nullable=False, default=True)

    transactions_from = db.relationship(
        "Transaction",
        foreign_keys="Transaction.purse_from_id",
        backref="purse_from",
        lazy="dynamic",
    )

    transactions_to = db.relationship(
        "Transaction",
        foreign_keys="Transaction.purse_to_id",
        backref="purse_to",
        lazy="dynamic",
    )

    def __init__(self, **kwargs):
        """
        Initializes a new purse instance.

        Args:
            - **kwargs: A dictionary of purse attributes.

        Raises:
            - ValueError: If the user_id attribute is not valid,
            or the currency attribute is not valid.

        """

        super().__init__(**kwargs)

        user = User.query.filter_by(id=self.user_id).first()
        if not user:
            logging.error("Purse creation failed. User doesn't exist.")
            raise ValueError("User doesn't exist.")

        if self.currency not in [c.value for c in Currency]:
            logging.error("Purse creation failed. Currency is not valid.")
            raise ValueError("Currency is not valid.")

    def __repr__(self):
        """
        Returns a string representation of the purse.

        Returns:
            - str: A string representing the purse.

        """

        return f"Purse id: {self.id}, \
            user_id: {self.user_id}, \
            currency: {self.currency}, \
            balance: {self.balance}"

    def date_created_str(self):
        """
        Converts the date_created attribute to a string.

        Returns:
            - str: A string representing the date_created
            attribute in the format "YYYY-MM-DD HH:MM:SS".

        """

        return self.date_created.strftime("%Y-%m-%d %H:%M:%S")

    def date_modified_str(self):
        """
        Converts the date_modified attribute to a string.

        Returns:
            - str: A string representing the date_modified
            attribute in the format "YYYY-MM-DD HH:MM:SS".

        """

        return self.date_modified.strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """
        Returns a dictionary representation of the purse.

        Returns:
            - dict: A dictionary representing the purse.

        """

        return {
            "id": self.id,
            "user_id": self.user_id,
            "currency": Currency(self.currency).value,
            "balance": self.balance,
            "date_created": self.date_created_str(),
            "date_modified": self.date_modified_str(),
        }

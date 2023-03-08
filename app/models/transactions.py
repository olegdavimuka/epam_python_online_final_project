"""
This module defines the Transaction class which represents a Transaction entity in the database.
It also contains functions for converting date and time objects to string representations.

Dependencies:
    - logging
    - datetime
    - app.db
    - app.constants.currency
    - app.constants.rates
    - app.models.purses

Exported classes:
    - Transaction

"""

import logging
from datetime import datetime

from app import db
from app.constants.currency import Currency
from app.constants.rates import Rates
from app.models.purses import Purse


class Transaction(db.Model):
    """
    A model that represents a transaction between two purses.

    Attributes:
        - __tablename__ (str): The name of the database table for this model.
        - id (int): The unique identifier of the transaction.
        - purse_from_id (int): The ID of the purse where the money comes from.
        - purse_to_id (int): The ID of the purse where the money goes to.
        - purse_from_currency (Currency): The currency of the purse where the money comes from.
        - purse_to_currency (Currency): The currency of the purse where the money goes to.
        - purse_from_amount (float): The amount of money that is being transferred from the purse.
        - purse_to_amount (float): The amount of money that is being transferred to the purse.
        - date_created (datetime): The date and time when the transaction was created.

    Methods:
        - __repr__(self): Returns a string representation of the transaction.
        - date_created_str(self): Converts the date_created attribute to a string.
        - to_dict(self): Returns a dictionary representation of the transaction.
        - update(self, **args): Updates the transaction with the provided values.

    """

    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)

    purse_from_id = db.Column(db.Integer, db.ForeignKey("purses.id"), nullable=False)
    purse_to_id = db.Column(db.Integer, db.ForeignKey("purses.id"), nullable=False)

    purse_from_currency = db.Column(db.Enum(Currency), nullable=False)
    purse_to_currency = db.Column(db.Enum(Currency), nullable=False)

    purse_from_amount = db.Column(db.Float, nullable=False, default=0.0)
    purse_to_amount = db.Column(db.Float, nullable=False, default=0.0)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        """
        Returns a string representation of the transaction.

        Returns:
            - str: A string representing the transaction.

        """

        return f"Transaction id: {self.id}, \
            purse_from_id: {self.purse_from_id}, \
            purse_to_id: {self.purse_to_id}, \
            purse_from_currency: {self.purse_from_currency}, \
            purse_to_currency: {self.purse_to_currency}, \
            purse_from_amount: {self.purse_from_amount}, \
            purse_to_amount: {self.purse_to_amount}"

    def date_created_str(self):
        """
        Converts the date_created attribute to a string.

        Returns:
            - str: A string representing the date_created
            attribute in the format "YYYY-MM-DD HH:MM:SS".

        """

        return self.date_created.strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """
        Returns a dictionary representation of the transaction.

        Returns:
            - dict: A dictionary representing the transaction.

        """

        return {
            "id": self.id,
            "purse_from_id": self.purse_from_id,
            "purse_to_id": self.purse_to_id,
            "purse_from_currency": Currency(self.purse_from_currency).value,
            "purse_to_currency": Currency(self.purse_to_currency).value,
            "purse_from_amount": self.purse_from_amount,
            "purse_to_amount": self.purse_to_amount,
            "date_created": self.date_created_str(),
        }

    def update(self, **kwargs):
        """
        Updates the Transaction object with the given keyword arguments

        Parameters:
            - **kwargs: Keyword arguments to update the Transaction object with.

        """
        purse_from = Purse.query.get_or_404(kwargs["purse_from_id"])
        purse_to = Purse.query.get_or_404(kwargs["purse_to_id"])
        purse_from_amount = float(kwargs["purse_from_amount"])

        kwargs["purse_from_currency"] = purse_from.currency
        kwargs["purse_to_currency"] = purse_to.currency

        if kwargs["purse_from_currency"] != kwargs["purse_to_currency"]:
            kwargs["purse_to_amount"] = purse_from_amount * Rates.get_rate(
                kwargs["purse_from_currency"], kwargs["purse_to_currency"]
            )
            logging.info(
                "Transaction creation success. Purse from currency %s \
                    is different from purse to currency %s. \
                    Purse to amount is calculated using the exchange rate.",
                kwargs["purse_from_currency"],
                kwargs["purse_to_currency"],
            )
        else:
            kwargs["purse_to_amount"] = purse_from_amount

        if purse_from.currency != purse_to.currency:
            purse_to_amount = kwargs["purse_to_amount"]
            purse_to.update(balance=purse_to.balance + purse_to_amount)
            purse_from.update(balance=purse_from.balance - purse_from_amount)
        else:
            purse_to.update(balance=purse_to.balance + purse_from_amount)
            purse_from.update(balance=purse_from.balance - purse_from_amount)

        logging.info(
            "Transaction creation success. Purse from balance is decreased by %s. \
                Purse to balance is increased by %s.",
            purse_from_amount,
            kwargs["purse_to_amount"],
        )
        db.session.commit()

        for key, value in kwargs.items():
            setattr(self, key, value)

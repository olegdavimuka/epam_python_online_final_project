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
        - __init__(self, **kwargs): Initializes a new transaction instance.
        - __repr__(self): Returns a string representation of the transaction.
        - date_created_str(self): Converts the date_created attribute to a string.
        - to_dict(self): Returns a dictionary representation of the transaction.

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

    def __init__(self, **kwargs):
        """
        Initializes a new transaction instance.

        Args:
            - **kwargs: Dictionary containing transaction attributes.

        Raises:
            - ValueError: If either the purse_from_id or purse_to_id do not exist,
            or if the purse_from_amount is greater than the balance of the purse_from.

        """

        super().__init__(**kwargs)

        purse_from = Purse.query.filter_by(id=self.purse_from_id).first()
        if not purse_from:
            logging.error("Transaction creation failed. Purse from doesn't exist.")
            raise ValueError("Purse from doesn't exist.")

        purse_to = Purse.query.filter_by(id=self.purse_to_id).first()
        if not purse_to:
            logging.error("Transaction creation failed. Purse to doesn't exist.")
            raise ValueError("Purse to doesn't exist.")

        if purse_from == purse_to:
            logging.error(
                "Transaction creation failed. Purse from and purse to are the same."
            )
            raise ValueError("Purse from and purse to are the same.")

        if purse_from.balance < self.purse_from_amount:
            logging.error(
                "Transaction creation failed. Purse from amount is not enough. \
                    (%s < %s))",
                purse_from.balance,
                self.purse_from_amount,
            )
            raise ValueError("Purse from amount is not enough.")

        self.purse_from_currency = purse_from.currency
        self.purse_to_currency = purse_to.currency

        if purse_from.currency != purse_to.currency:
            self.purse_to_amount = self.purse_from_amount * Rates.get_rate(
                self.purse_from_currency, self.purse_to_currency
            )
            logging.info(
                "Transaction creation success. Purse from currency %s \
                    is different from purse to currency %s. \
                    Purse to amount is calculated using the exchange rate.",
                self.purse_from_currency,
                self.purse_to_currency,
            )
        else:
            self.purse_to_amount = self.purse_from_amount

        purse_from.balance -= self.purse_from_amount
        purse_to.balance += self.purse_to_amount
        logging.info(
            "Transaction creation success. Purse from balance is decreased by %s. \
                Purse to balance is increased by %s.",
            self.purse_from_amount,
            self.purse_to_amount,
        )
        db.session.commit()

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

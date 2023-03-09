"""
This module contains the tests for the Transaction model class.

Dependencies:
    - datetime
    - app.constants.currency
    - app.tests.models.fixtures

Classes:
    - TestTransactionModel: A class that contains the tests for the Transaction model class.

"""


from datetime import datetime

from app.constants.currency import Currency
from app.tests.models.fixtures import (  # noqa: F401 pylint: disable=unused-import
    fixture_transaction,
)


class TestTransactionModel:
    """
    This class contains the tests for the Transaction model class.

    Methods:
        - test_transaction_creation(): tests the creation of a transaction.
        - test_transaction_representation(): tests the __repr__() method.
        - test_transaction_date_conversion(): tests the date_created_str() and date_modified_str()
        methods.
        - test_transaction_dict_conversion(): tests the to_dict() method.

    """

    def test_transaction_creation(self, transaction):
        """
        Test the creation of a transaction.

        Args:
            - transaction: A transaction object.

        """

        assert transaction.purse_from_id == 1
        assert transaction.purse_to_id == 2
        assert transaction.purse_from_currency == Currency.USD
        assert transaction.purse_to_currency == Currency.EUR
        assert transaction.purse_from_amount == 100.0
        assert transaction.purse_to_amount == 95
        assert transaction.date_created == datetime(2022, 3, 8, 12, 0, 0)

    def test_transaction_representation(self, transaction):
        """
        Test the __repr__() method.

        Args:
            - transaction: A transaction object.

        """

        assert (
            repr(transaction)
            == "Transaction id: None, \
            purse_from_id: 1, \
            purse_to_id: 2, \
            purse_from_currency: Currency.USD, \
            purse_to_currency: Currency.EUR, \
            purse_from_amount: 100.0, \
            purse_to_amount: 95.0"
        )

    def test_transaction_date_conversion(self, transaction):
        """
        Test the date_created_str() method.

        Args:
            - transaction: A transaction object.

        """

        assert transaction.date_created_str() == "2022-03-08 12:00:00"

    def test_transaction_dict_conversion(self, transaction):
        """
        Test the to_dict() method.

        Args:
            - transaction: A transaction object.

        """

        transaction_dict = transaction.to_dict()
        assert transaction_dict["purse_from_id"] == 1
        assert transaction_dict["purse_to_id"] == 2
        assert transaction_dict["purse_from_currency"] == "USD"
        assert transaction_dict["purse_to_currency"] == "EUR"
        assert transaction_dict["purse_from_amount"] == 100.0
        assert transaction_dict["purse_to_amount"] == 95
        assert transaction_dict["date_created"] == "2022-03-08 12:00:00"

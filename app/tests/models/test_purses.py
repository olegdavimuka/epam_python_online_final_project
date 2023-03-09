"""
This module contains the tests for the Purse model class.

Dependencies:
    - datetime
    - app.constants.currency
    - app.tests.models.fixtures

Classes:
    - TestPurseModel: A class that contains the tests for the Purse model class.

"""


from datetime import datetime

from app.constants.currency import Currency
from app.tests.models.fixtures import (  # noqa: F401 pylint: disable=unused-import
    fixture_purse,
)


class TestPurseModel:
    """
    This class contains the tests for the Purse model class.

    Methods:
        - test_purse_creation(): tests the creation of a purse.
        - test_purse_representation(): tests the __repr__() method.
        - test_purse_date_conversion(): tests the date_created_str() and date_modified_str()
        methods.
        - test_purse_dict_conversion(): tests the to_dict() method.
        - test_purse_update(): tests the update() method.

    """

    def test_purse_creation(self, purse):
        """
        Test the creation of a purse.

        Args:
            - purse: A Purse object.

        """

        assert purse.user_id == 1
        assert purse.currency == Currency.USD
        assert purse.balance == 100.0
        assert purse.date_created == datetime(2022, 3, 8, 12, 0, 0)
        assert purse.date_modified == datetime(2022, 3, 8, 12, 0, 0)
        assert purse.is_active is True

    def test_purse_representation(self, purse):
        """
        Test the __repr__() method.

        Args:
            - purse: A Purse object.

        """

        assert (
            repr(purse)
            == "Purse id: None, \
            user_id: 1, \
            currency: Currency.USD, \
            balance: 100.0"
        )

    def test_purse_date_conversion(self, purse):
        """
        Test the date_created_str() and date_modified_str() methods.

        Args:
            - purse: A Purse object.

        """

        assert purse.date_created_str() == "2022-03-08 12:00:00"
        assert purse.date_modified_str() == "2022-03-08 12:00:00"

    def test_purse_dict_conversion(self, purse):
        """
        Test the to_dict() method.

        Args:
            - purse: A Purse object.

        """

        purse_dict = purse.to_dict()
        assert purse_dict["user_id"] == 1
        assert purse_dict["currency"] == "USD"
        assert purse_dict["balance"] == 100.0
        assert purse_dict["date_created"] == "2022-03-08 12:00:00"
        assert purse_dict["date_modified"] == "2022-03-08 12:00:00"

    def test_purse_update(self, purse):
        """
        Test the update() method.

        Args:
            - purse: A Purse object.

        """

        purse.update(balance=200.0, is_active=False)
        assert purse.balance == 200.0
        assert purse.is_active is False

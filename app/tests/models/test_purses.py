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
from app.tests.fixtures import (  # noqa: F401 pylint: disable=unused-import
    fixture_app,
    fixture_client,
    fixture_purse,
    fixture_user,
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
        assert purse.balance == 900.0
        assert purse.date_created.date() == datetime.now().date()
        assert purse.date_modified.date() == datetime.now().date()
        assert purse.is_active is True

    def test_purse_representation(self, purse):
        """
        Test the __repr__() method.

        Args:
            - purse: A Purse object.

        """

        assert (
            repr(purse)
            == "Purse id: 1, \
            user_id: 1, \
            currency: Currency.USD, \
            balance: 900.0"
        )

    def test_purse_date_conversion(self, purse):
        """
        Test the date_created_str() and date_modified_str() methods.

        Args:
            - purse: A Purse object.

        """

        assert purse.date_created_str().split(" ")[0] == datetime.now().strftime(
            "%Y-%m-%d"
        )
        assert purse.date_modified_str().split(" ")[0] == datetime.now().strftime(
            "%Y-%m-%d"
        )

    def test_purse_dict_conversion(self, purse):
        """
        Test the to_dict() method.

        Args:
            - purse: A Purse object.

        """

        purse_dict = purse.to_dict()
        assert purse_dict["user_id"] == 1
        assert purse_dict["currency"] == "USD"
        assert purse_dict["balance"] == 900.0
        assert purse.date_created_str().split(" ")[0] == datetime.now().strftime(
            "%Y-%m-%d"
        )
        assert purse.date_modified_str().split(" ")[0] == datetime.now().strftime(
            "%Y-%m-%d"
        )

    def test_purse_update(self, purse):
        """
        Test the update() method.

        Args:
            - purse: A Purse object.

        """

        purse.update(balance=200.0, is_active=False)
        assert purse.balance == 200.0
        assert purse.is_active is False

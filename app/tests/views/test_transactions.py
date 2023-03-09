"""
This module contains the tests for the transactions view.

Dependencies:
    - datetime
    - faker
    - app.constants.currency
    - app.models.api.fixtures

Classes:
    - TestTransactionsView: A class that contains the tests for the transactions view.

"""

from datetime import datetime

from faker import Faker

from app.constants.currency import Currency
from app.tests.fixtures import (  # noqa: F401 pylint: disable=unused-import
    fixture_app,
    fixture_client,
    fixture_purse,
    fixture_purses,
    fixture_transaction,
    fixture_user,
)

fake = Faker()


class TestTransactionsView:
    """
    This class contains the tests for the transactions view.

    Methods:
        - test_list_transactions(client, transaction): tests the retrieval of all transactions.
        - test_get_transaction(client, transaction): tests the retrieval of a transaction with a
        given ID.
        - test_create_transaction(client, purses): tests the creation of a transaction.

    """

    def test_list_transactions(self, client, transaction):
        """
        Test retrieving a list of transactions.

        Args:
            - client: The test client.
            - transaction: The transaction instance.

        """

        response = client.get("/transactions/")
        assert response.status_code == 200
        assert b"Transaction" in response.data
        assert str(transaction.id) in response.data.decode("utf-8")
        assert str(transaction.purse_from_id) in response.data.decode("utf-8")
        assert str(transaction.purse_to_id) in response.data.decode("utf-8")
        assert transaction.purse_from_currency.value in response.data.decode("utf-8")
        assert transaction.purse_to_currency.value in response.data.decode("utf-8")
        assert str(transaction.purse_from_amount) in response.data.decode("utf-8")
        assert str(transaction.purse_to_amount) in response.data.decode("utf-8")
        assert datetime.strftime(datetime.now(), "%Y-%m-%d") in response.data.decode(
            "utf-8"
        )
        assert transaction.query.count() == 1

    def test_get_transaction(self, client, transaction):
        """
        Test retrieving a transaction with a given ID.

        Args:
            - client: The test client.
            - transaction: The transaction instance.

        """

        response = client.get("/transactions/1")
        assert response.status_code == 200
        assert str(transaction.id) in response.data.decode("utf-8")
        assert str(transaction.purse_from_id) in response.data.decode("utf-8")
        assert str(transaction.purse_to_id) in response.data.decode("utf-8")
        assert transaction.purse_from_currency.value in response.data.decode("utf-8")
        assert transaction.purse_to_currency.value in response.data.decode("utf-8")
        assert str(transaction.purse_from_amount) in response.data.decode("utf-8")
        assert str(transaction.purse_to_amount) in response.data.decode("utf-8")
        assert datetime.strftime(datetime.now(), "%Y-%m-%d") in response.data.decode(
            "utf-8"
        )

    def test_create_transaction(self, client, purses):
        """
        Test creating a new transaction.

        Args:
            - client: The test client.
            - purses: The list of purses.

        """

        data = {
            "purse_from_id": purses[0].id,
            "purse_to_id": purses[1].id,
            "purse_from_amount": 100,
        }

        response = client.post("/transactions/0", data=data)
        assert response.status_code == 200
        assert str(purses[0].id) in response.data.decode("utf-8")
        assert str(purses[1].id) in response.data.decode("utf-8")
        assert Currency(purses[0].currency).value in response.data.decode("utf-8")
        assert Currency(purses[1].currency).value in response.data.decode("utf-8")
        assert "100" in response.data.decode("utf-8")
        assert "95" in response.data.decode("utf-8")  # Rate = 0.95

        assert purses[0].balance == 800  # purse1.balance = 900 - 100 = 800
        assert purses[1].balance == 1190  # purse2.balance = 1095 + 95 = 1190

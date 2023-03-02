"""
This module contains the tests for the transactions API.

Dependencies:
    - faker
    - app.constants.currency
    - app.models.api.fixtures

Classes:
    - TestTransactionsAPI: A class that contains the tests for the transactions API.

"""

from faker import Faker

from app.constants.currency import Currency
from app.tests.api.fixtures import (  # noqa: F401 pylint: disable=unused-import
    fixture_app, fixture_client, fixture_purse, fixture_purses, fixture_runner,
    fixture_transaction, fixture_user)

fake = Faker()


class TestTransactionsAPI:
    """
    This class contains the tests for the transactions API.

    Methods:
        - test_get_transactions(client, transactions): tests the retrieval of all transactions.
        - test_get_transaction(client, transactions): tests the retrieval of a transaction.
        - test_get_nonexistent_transaction(client): tests the retrieval of a
        nonexistent transaction.
        - test_post_transaction(client): tests the creation of a transaction
        - test_post_transaction_invalid_purse_from(client): tests the creation of a
        transaction with an invalid purse_from.
        - test_post_transaction_invalid_purse_to(client): tests the creation of a
        transaction with an invalid purse_to.
        - test_post_transaction_not_enough_funds(client): tests the creation of a
        transaction with not enough funds.
        - test_post_transaction_same_purse(client): tests the creation of a
        transaction with the same purse_from and purse_to.

    """

    def test_get_transactions(self, client, transaction):
        """
        Test retrieving all transactions.

        Args:
            - client: The test client.
            - transaction: The transaction instance.

        """

        response = client.get("/api/transactions")
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["id"] == transaction.id
        assert response.json[0]["purse_from_id"] == transaction.purse_from_id
        assert response.json[0]["purse_to_id"] == transaction.purse_to_id
        assert (
            response.json[0]["purse_from_currency"]
            == Currency(transaction.purse_from_currency).value
        )
        assert (
            response.json[0]["purse_to_currency"]
            == Currency(transaction.purse_to_currency).value
        )
        assert response.json[0]["purse_from_amount"] == transaction.purse_from_amount
        assert response.json[0]["purse_to_amount"] == transaction.purse_to_amount

    def test_get_transaction(self, client, transaction):
        """
        Test retrieving a transaction with a given ID.

        Args:
            - client: The test client.
            - transaction: The transaction instance.

        """

        response = client.get(f"/api/transactions/{transaction.id}")
        assert response.status_code == 200
        assert response.json["id"] == transaction.id
        assert response.json["purse_from_id"] == transaction.purse_from_id
        assert response.json["purse_to_id"] == transaction.purse_to_id
        assert (
            response.json["purse_from_currency"]
            == Currency(transaction.purse_from_currency).value
        )
        assert (
            response.json["purse_to_currency"]
            == Currency(transaction.purse_to_currency).value
        )
        assert response.json["purse_from_amount"] == transaction.purse_from_amount
        assert response.json["purse_to_amount"] == transaction.purse_to_amount

    def test_get_nonexistent_transaction(self, client):
        """
        Test retrieving a nonexistent transaction.

        Args:
            - client: The test client.

        """

        response = client.get("/api/transactions/0")
        assert response.status_code == 404

    def test_post_transaction(self, client, purses):
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

        response = client.post("/api/transactions", data=data)
        assert response.status_code == 201
        assert response.json["purse_from_id"] == purses[0].id
        assert response.json["purse_to_id"] == purses[1].id
        assert (
            response.json["purse_from_currency"] == Currency(purses[0].currency).value
        )
        assert response.json["purse_to_currency"] == Currency(purses[1].currency).value
        assert response.json["purse_from_amount"] == 100
        assert response.json["purse_to_amount"] == 95  # 100 * 0.95

        assert purses[0].balance == 800
        assert purses[1].balance == 1190

    def test_post_transaction_invalid_purse_from(self, client, purse):
        """
        Test creating a new transaction with an invalid purse.

        Args:
            - client: The test client.
            - purse: The purse instance.

        """

        data = {
            "purse_from_id": 0,
            "purse_to_id": purse.id,
            "purse_from_amount": 100,
        }

        response = client.post("/api/transactions", data=data)
        assert response.status_code == 400

    def test_post_transaction_invalid_purse_to(self, client, purse):
        """
        Test creating a new transaction with an invalid purse.

        Args:
            - client: The test client.
            - purse: The purse instance.

        """

        data = {
            "purse_from_id": purse.id,
            "purse_to_id": 0,
            "purse_from_amount": 100,
        }

        response = client.post("/api/transactions", data=data)
        assert response.status_code == 400

    def test_post_transaction_not_enough_funds(self, client, purses):
        """
        Test creating a new transaction with not enough funds.

        Args:
            - client: The test client.
            - purses: The list of purses.

        """

        data = {
            "purse_from_id": purses[0].id,
            "purse_to_id": purses[1].id,
            "purse_from_amount": 10000,
        }

        response = client.post("/api/transactions", data=data)
        assert response.status_code == 400

    def test_post_transaction_same_purse(self, client, purse):
        """
        Test creating a new transaction with the same purse.

        Args:
            - client: The test client.
            - purse: The purse instance.

        """

        data = {
            "purse_from_id": purse.id,
            "purse_to_id": purse.id,
            "purse_from_amount": 100,
        }

        response = client.post("/api/transactions", data=data)
        assert response.status_code == 400

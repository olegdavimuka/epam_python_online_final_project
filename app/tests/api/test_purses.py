"""
This module contains the tests for the purses API.

Dependencies:
    - faker
    - app.constants.currency
    - app.models.purses
    - app.tests.fixtures

Classes:
    - TestPursesAPI: A class that contains the tests for the purses API.

"""

from faker import Faker

from app.constants.currency import Currency
from app.models.purses import Purse
from app.tests.fixtures import (  # noqa: F401 pylint: disable=unused-import
    fixture_app,
    fixture_client,
    fixture_purse,
    fixture_user,
)

fake = Faker()


class TestPursesAPI:
    """
    This class contains the tests for the purses API.

    Methods:
        - test_get_purses(client, purse): tests the retrieval of all purses.
        - test_get_purse(client, purse): tests the retrieval of a purse with a given
        - test_get_nonexistent_purse(client): tests the retrieval of a nonexistent purse.
        - test_delete_purse(client, purse): tests the deletion of a purse with a given
        - test_test_delete_nonexistent_purse(client): tests the deletion of a nonexistent
        - test_post_purse(client, user): tests the creation of a purse.
        - test_post_purse_with_invalid_user_id(client): tests the creation of a purse with an
        invalid user ID.
        - test_post_purse_with_invalid_currency(client, user): tests the creation of a purse with
        an invalid currency.

    """

    def test_get_purses(self, client, purse):
        """
        Test retrieving all purses.

        Args:
            - client: The test client.
            - purse: The purse instance.

        """

        response = client.get("/api/purses/")
        assert response.status_code == 200
        assert len(response.json) == 3
        assert response.json[0]["id"] == purse.id
        assert response.json[0]["user_id"] == purse.user_id
        assert response.json[0]["currency"] == Currency(purse.currency).value
        assert response.json[0]["balance"] == purse.balance

    def test_get_purse(self, client, purse):
        """
        Test retrieving a purse with a given ID.

        Args:
            - client: The test client.
            - purse: The purse instance.

        """

        response = client.get(f"/api/purses/{purse.id}")
        assert response.status_code == 200
        assert response.json["id"] == purse.id
        assert response.json["user_id"] == purse.user_id
        assert response.json["currency"] == Currency(purse.currency).value
        assert response.json["balance"] == purse.balance

    def test_get_nonexistent_purse(self, client):
        """
        Test retrieving a nonexistent user.

        Args:
            - client: The test client.

        """

        response = client.get("/api/purses/0")
        assert response.status_code == 404

    def test_delete_purse(self, client, purse):
        """
        Test deleting a purse with a given ID.

        Args:
            - client: The test client.
            - purse: The purse instance.

        """

        response = client.delete(f"/api/purses/{purse.id}")
        assert response.status_code == 204
        assert Purse.query.filter_by(id=purse.id).count() == 1
        assert Purse.query.filter_by(id=purse.id).first().is_active is False

    def test_delete_nonexistent_purse(self, client):
        """
        Test deleting a nonexistent purse.

        Args:
            - client: The test client.

        """

        response = client.delete("/api/purses/0")
        assert response.status_code == 404

    def test_post_purse(self, client, user):
        """
        Test creating a new purse.

        Args:
            - client: The test client.
            - user: The user instance.

        """

        data = {
            "user_id": user.id,
            "currency": Currency.USD.value,
        }

        response = client.post("/api/purses/", data=data)
        assert response.status_code == 201
        assert response.json["user_id"] == user.id
        assert response.json["currency"] == Currency.USD.value
        assert response.json["balance"] == 0.0

    def test_post_purse_with_invalid_user_id(self, client):
        """
        Test creating a purse with an invalid user id.

        Args:
            - client: The test client.

        """

        data = {
            "user_id": 0,
            "currency": Currency.USD,
        }

        response = client.post("/api/purses/", data=data)
        assert response.status_code == 400

    def test_post_purse_with_invalid_currency(self, client, user):
        """
        Test creating a purse with an invalid currency.

        Args:
            - client: The test client.
            - user: The user instance.

        """

        data = {
            "user_id": user.id,
            "currency": "invalid",
        }

        response = client.post("/api/purses/", data=data)
        assert response.status_code == 400

"""
This module contains the tests for the purses view.

Dependencies:
    - datetime
    - app.constants.currency
    - app.models.purses
    - app.tests.fixtures

Classes:
    - TestPursesView: A class that contains the tests for the purses view.

"""

from datetime import datetime

from app.constants.currency import Currency
from app.models.purses import Purse
from app.tests.fixtures import (  # noqa: F401 pylint: disable=unused-import
    fixture_app,
    fixture_client,
    fixture_purse,
    fixture_user,
)


class TestPursesView:
    """
    This class contains the tests for the purses view.

    Methods:
        - test_list_purses(client, purse): tests the retrieval of all purses.
        - test_get_purse(client, purse): tests the retrieval of a purse with a given ID.
        - test_create_purse(client, user): tests the creation of a purse.
        - test_delete_purse(client, purse): tests the deletion of a purse with a given ID.

    """

    def test_list_purses(self, client, purse):
        """
        Test retrieving a list of purses.

        Args:
            - client: The test client.
            - purse: The purse instance.

        """

        response = client.get("/purses/")
        assert response.status_code == 200
        assert b"Purses" in response.data
        assert str(purse.id) in response.data.decode("utf-8")
        assert str(purse.user_id) in response.data.decode("utf-8")
        assert purse.currency.value in response.data.decode("utf-8")
        assert str(purse.balance) in response.data.decode("utf-8")
        assert datetime.strftime(datetime.now(), "%Y-%m-%d") in response.data.decode(
            "utf-8"
        )
        assert Purse.query.count() == 2

    def test_get_purse(self, client, purse):
        """
        Test retrieving a purse with a given ID.

        Args:
            - client: The test client.
            - purse: The purse instance.

        """

        response = client.get("/purses/1")
        assert response.status_code == 200
        assert str(purse.id) in response.data.decode("utf-8")
        assert str(purse.user_id) in response.data.decode("utf-8")
        assert purse.currency.value in response.data.decode("utf-8")
        assert str(purse.balance) in response.data.decode("utf-8")
        assert datetime.strftime(datetime.now(), "%Y-%m-%d") in response.data.decode(
            "utf-8"
        )

    def test_create_purse(self, client, user):
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

        response = client.post("purses/0", data=data)
        assert response.status_code == 200
        assert str(user.id) in response.data.decode("utf-8")
        assert Currency.USD.value in response.data.decode("utf-8")
        assert "0.0" in response.data.decode("utf-8")
        assert datetime.strftime(datetime.now(), "%Y-%m-%d") in response.data.decode(
            "utf-8"
        )
        assert Purse.query.count() == 3

    def test_delete_purse(self, client, purse):
        """
        Test deleting a purse with a given ID.

        Args:
            - client: The test client.
            - purse: The purse instance.

        """

        count_before = Purse.query.count()
        response = client.delete(f"/purses/{purse.id}")
        assert response.status_code == 200
        count_after = Purse.query.count()
        assert count_before == count_after
        assert Purse.query.filter_by(is_active=True).count() == count_before - 1

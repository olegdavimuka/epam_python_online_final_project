"""
This module contains the tests for the Home view.

Dependencies:
    - app.constants.rates
    - app.tests.views.fixtures

Classes:
    - TestHomeView: A class that contains the tests for the Home view.

"""

from app.constants.rates import Currency, Rates
from app.tests.fixtures import (  # noqa: F401 pylint: disable=unused-import
    fixture_app,
    fixture_client,
)


class TestHomeView:
    """
    This class contains the tests for the Home view.

    Methods:
        - test_home_page(): tests the home page.

    """

    def test_home_page(self, client):
        """
        Test the home page.

        Args:
            - client: A Flask test client.

        """

        response = client.get("/")
        assert response.status_code == 200
        assert b"Rates" in response.data
        assert b"Currency" in response.data
        assert b"USD" in response.data
        assert b"EUR" in response.data
        assert b"GBP" in response.data
        assert b"UAH" in response.data
        assert Currency.USD.value in response.data.decode("utf-8")
        assert Currency.EUR.value in response.data.decode("utf-8")
        assert Currency.GBP.value in response.data.decode("utf-8")
        assert Currency.UAH.value in response.data.decode("utf-8")

    def test_currency_conversion(self, client):
        """
        Test the currency conversion.
        
        Args:
            - client: A Flask test client.
            
        """
        response = client.get("/")
        assert str(Rates.get_rate(Currency.USD, Currency.USD)) in response.data.decode(
            "utf-8"
        )
        assert str(Rates.get_rate(Currency.USD, Currency.EUR)) in response.data.decode(
            "utf-8"
        )
        assert str(Rates.get_rate(Currency.USD, Currency.GBP)) in response.data.decode(
            "utf-8"
        )
        assert str(Rates.get_rate(Currency.USD, Currency.UAH)) in response.data.decode(
            "utf-8"
        )

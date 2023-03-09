"""
This module contains the tests for the PurseForm class.

Dependencies:
    - app.forms.purse
    - app.tests.forms.fixtures

Classes:
    - TestPurseForm: A class that contains the tests for the PurseForm class.

"""

from app.forms.purses import PurseForm, SearchForm
from app.tests.forms.fixtures import (  # noqa: F401 pylint: disable=unused-import
    fixture_app,
)


class TestPurseForm:
    """
    This class contains the tests for the PurseForm class.

    Methods:
        - test_search_form(): tests the SearchForm class.
        - test_purse_form(): tests the PurseForm class.

    """

    def test_search_form(self, app):
        """
        Test the SearchForm class.

        Args:
            - app: A Flask app object.

        """

        with app.test_request_context():
            form = SearchForm()

            assert hasattr(form, "search")
            assert hasattr(form, "date_created")
            assert hasattr(form, "date_modified")
            assert hasattr(form, "user_id")
            assert hasattr(form, "currency")

            assert form.validate() is True

            form = SearchForm(
                search="test",
                date_created="2022-01-01",
                date_modified="2022-01-02",
                user_id="1",
                currency="USD",
            )

            assert form.search.data == "test"
            assert form.date_created.data == "2022-01-01"
            assert form.date_modified.data == "2022-01-02"
            assert form.user_id.data == "1"
            assert form.currency.data == "USD"

            assert form.validate() is True

    def test_purse_form(self, app):
        """
        Test the PurseForm class.

        Args:
            - app: A Flask app object.

        """

        with app.test_request_context():
            form = PurseForm()

            assert hasattr(form, "user_id")
            assert hasattr(form, "currency")
            assert hasattr(form, "balance")
            assert hasattr(form, "date_created")
            assert hasattr(form, "date_modified")

            assert form.validate() is True

            form = PurseForm(
                user_id="1",
                currency="USD",
                balance="100.00",
            )

            assert form.currency.data == "USD"
            assert form.balance.data == "100.00"
            assert form.user_id.data == "1"

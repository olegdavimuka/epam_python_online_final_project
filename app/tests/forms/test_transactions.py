"""
This module contains the tests for the TransactionForm class.

Dependencies:
    - app.forms.transactions
    - app.tests.forms.fixtures

Classes:
    - TestTransactionForm: A class that contains the tests for the TransactionForm class.

"""

from app.forms.transactions import SearchForm, TransactionForm
from app.tests.fixtures import fixture_app  # noqa: F401 pylint: disable=unused-import


class TestTransactionForm:
    """
    This class contains the tests for the TransactionForm class.

    Methods:
        - test_search_form(): tests the SearchForm class.
        - test_transaction_form(): tests the TransactionForm class.

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
            assert hasattr(form, "purse_from_id")
            assert hasattr(form, "purse_to_id")
            assert hasattr(form, "purse_from_currency")
            assert hasattr(form, "purse_to_currency")

            assert form.validate() is True

            form = SearchForm(
                search="test",
                date_created="2022-01-01",
                date_modified="2022-01-02",
                purse_from_id="1",
                purse_to_id="2",
                purse_from_currency="USD",
                purse_to_currency="USD",
            )

            assert form.search.data == "test"
            assert form.date_created.data == "2022-01-01"
            assert form.date_modified.data == "2022-01-02"
            assert form.purse_from_id.data == "1"
            assert form.purse_to_id.data == "2"
            assert form.purse_from_currency.data == "USD"
            assert form.purse_to_currency.data == "USD"

            assert form.validate() is True

    def test_transaction_form(self, app):
        """
        Test the TransactionForm class.

        Args:
            - app: A Flask app object.

        """

        with app.test_request_context():
            form = TransactionForm()

            assert hasattr(form, "purse_from_id")
            assert hasattr(form, "purse_to_id")
            assert hasattr(form, "purse_from_amount")
            assert hasattr(form, "purse_to_amount")
            assert hasattr(form, "date_created")

            assert form.validate() is False
            assert "purse_from_amount" in form.errors

            form = TransactionForm(
                purse_from_id="1",
                purse_to_id="2",
                purse_from_amount="100",
                purse_to_amount="100",
                date_created="2022-01-01",
            )

            assert form.purse_from_id.data == "1"
            assert form.purse_to_id.data == "2"
            assert form.purse_from_amount.data == "100"
            assert form.purse_to_amount.data == "100"
            assert form.date_created.data == "2022-01-01"

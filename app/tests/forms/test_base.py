"""
This module contains the tests for the BaseSearchForm class.

Dependencies:
    - app.forms.base
    - app.tests.forms.fixtures

Classes:
    - TestBaseSearchForm: A class that contains the tests for the BaseSearchForm class.

"""

from app.forms.base import BaseSearchForm
from app.tests.fixtures import fixture_app  # noqa: F401 pylint: disable=unused-import


class TestBaseSearchForm:
    """
    This class contains the tests for the BaseSearchForm class.

    Methods:
        - test_base_search_form(app): tests the BaseSearchForm class.
        - test_base_search_form_with_data(app): tests the BaseSearchForm class with data.

    """

    def test_base_search_form(self, app):
        """
        Test the BaseSearchForm class.

        Args:
            - app: A Flask app object.

        """

        with app.test_request_context():
            form = BaseSearchForm()
            assert form.search is not None
            assert form.date_created is not None
            assert form.date_modified is not None
            assert form.validate() is True

    def test_base_search_form_with_data(self, app):
        """
        Test the BaseSearchForm class with data.

        Args:
            - app: A Flask app object.

        """

        with app.test_request_context():
            data = {
                "search": "test",
                "date_created": "2022-01-01",
                "date_modified": "2022-02-01",
            }
            form = BaseSearchForm(data=data)
            assert form.search.data == "test"
            assert form.date_created.data == "2022-01-01"
            assert form.date_modified.data == "2022-02-01"
            assert form.validate() is True

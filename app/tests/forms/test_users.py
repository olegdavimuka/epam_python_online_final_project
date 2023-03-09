"""
This module contains the tests for the UserForm class.

Dependencies:
    - app.forms.users
    - app.tests.forms.fixtures

Classes:
    - TestUserForm: A class that contains the tests for the UserForm class.

"""

from app.forms.users import SearchForm, UserForm
from app.tests.forms.fixtures import (  # noqa: F401 pylint: disable=unused-import
    fixture_app,
)


class TestUserForm:
    """
    This class contains the tests for the UserForm class.

    Methods:
        - test_search_form(): tests the SearchForm class.
        - test_user_form(): tests the UserForm class.

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
            assert hasattr(form, "birth_date")

            assert form.validate() is True

            form = SearchForm(
                search="test",
                date_created="2022-01-01",
                date_modified="2022-01-02",
                birth_date="1990-01-01",
            )

            assert form.search.data == "test"
            assert form.date_created.data == "2022-01-01"
            assert form.date_modified.data == "2022-01-02"
            assert form.birth_date.data == "1990-01-01"

            assert form.validate() is True

    def test_user_form(self, app):
        """
        Test the UserForm class.

        Args:
            - app: A Flask app object.

        """

        with app.test_request_context():
            form = UserForm()

            assert hasattr(form, "username")
            assert hasattr(form, "email")
            assert hasattr(form, "phone")
            assert hasattr(form, "first_name")
            assert hasattr(form, "last_name")
            assert hasattr(form, "birth_date")
            assert hasattr(form, "date_created")
            assert hasattr(form, "date_modified")

            assert form.validate() is False
            assert "username" in form.errors
            assert "email" in form.errors
            assert "phone" in form.errors
            assert "first_name" in form.errors
            assert "last_name" in form.errors
            assert "birth_date" in form.errors

            form = UserForm(
                username="testuser",
                email="testuser@gmail.com",
                phone="+380123456789",
                first_name="John",
                last_name="Doe",
                birth_date="2000-01-01",
                date_created="2020-01-01",
                date_modified="2020-01-01",
            )

            assert form.username.data == "testuser"
            assert form.email.data == "testuser@gmail.com"
            assert form.phone.data == "+380123456789"
            assert form.first_name.data == "John"
            assert form.last_name.data == "Doe"
            assert form.birth_date.data == "2000-01-01"
            assert form.date_created.data == "2020-01-01"
            assert form.date_modified.data == "2020-01-01"

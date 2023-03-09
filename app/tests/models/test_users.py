"""
This module contains the tests for the User model class.

Dependencies:
    - datetime
    - app.tests.models.fixtures

Classes:
    - TestUserModel: A class that contains the tests for the User model class.

"""

from datetime import datetime

from app.tests.fixtures import (  # noqa: F401 pylint: disable=unused-import
    fixture_app,
    fixture_client,
    fixture_user,
)


class TestUserModel:
    """
    This class contains the tests for the User model class.

    Methods:
        - test_user_creation(): tests the creation of a user.
        - test_user_representation(): tests the __repr__() method.
        - test_birth_date_str(): tests the birth_date_str() method.
        - test_date_created_str(): tests the date_created_str() method.
        - test_date_modified_str(): tests the date_modified_str() method.
        - test_to_dict(): tests the to_dict() method.
        - test_update(): tests the update() method.

    """

    def test_user_creation(self, user):
        """
        Test the creation of a user.

        Args:
            - user: A User object.

        """

        assert user.username is not None
        assert user.email is not None
        assert user.phone is not None
        assert user.first_name is not None
        assert user.last_name is not None
        assert user.birth_date is not None

    def test_user_representation(self, user):
        """
        Test the __repr__() method.

        Args:
            - user: A User object.

        """

        assert (
            repr(user)
            == f"User id: 1, \
            name: {user.username}, \
            email: {user.email}, \
            phone: {user.phone}"
        )

    def test_birth_date_str(self, user):
        """
        Test the birth_date_str() method.

        Args:
            - user: A User object.

        """

        assert isinstance(user.birth_date_str(), str)

    def test_date_created_str(self, user):
        """
        Test the date_created_str() method.

        Args:
            - user: A User object.

        """

        assert isinstance(user.date_created_str(), str)

    def test_date_modified_str(self, user):
        """
        Test the date_modified_str() method.

        Args:
            - user: A User object.

        """

        assert isinstance(user.date_modified_str(), str)

    def test_to_dict(self, user):
        """
        Test the to_dict() method.

        Args:
            - user: A User object.

        """

        expected_dict = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "birth_date": user.birth_date_str(),
            "date_created": user.date_created_str(),
            "date_modified": user.date_modified_str(),
        }
        assert user.to_dict() == expected_dict

    def test_update(self, user):
        """
        Test the update() method.

        Args:
            - user: A User object.

        """

        user.update(username="newtestuser", birth_date="1999-12-31")
        assert user.username == "newtestuser"
        assert user.birth_date == datetime(1999, 12, 31)

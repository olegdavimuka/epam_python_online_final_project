"""
This module contains the tests for the User model class.

Dependencies:
    - datetime
    - app.tests.models.fixtures

Classes:
    - TestUserModel: A class that contains the tests for the User model class.

"""

from datetime import datetime

from app.tests.models.fixtures import (  # noqa: F401 pylint: disable=unused-import
    fixture_client,
    fixture_user,
)


class TestUserModel:
    """
    This class contains the tests for the User model class.

    Methods:
        - test_user_creation(): tests the creation of a user.
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

        assert user.username == "testuser"
        assert user.email == "testuser@example.com"
        assert user.phone == "123-456-7890"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.birth_date == datetime(2000, 1, 1).date()

    def test_birth_date_str(self, user):
        """
        Test the birth_date_str() method.

        Args:
            - user: A User object.

        """

        assert user.birth_date_str() == "2000-01-01"

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

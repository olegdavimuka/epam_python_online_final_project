"""
This module contains the tests for the users view.

Dependencies:
    - datetime
    - faker
    - app.models.users
    - app.tests.views.fixtures
    - app.utils.validation

Classes:
    - TestUsersView: A class that contains the tests for the users view.

"""

from datetime import datetime

from faker import Faker

from app.models.users import User
from app.tests.fixtures import (  # noqa: F401 pylint: disable=unused-import
    fixture_app,
    fixture_client,
    fixture_user,
)
from app.utils.validation import fake_phone_number

fake = Faker()


class TestUsersView:
    """
    This class contains the tests for the users view.

    Methods:
        - test_list_users(client, user): tests the retrieval of all users.
        - test_get_user(client, user): tests the retrieval of a user with a given ID.
        - test_get_nonexistent_user(client, user): tests the retrieval of a user that does not'
        exist.
        - test_create_user(client): tests the creation of a new user.
        - test_edit_user(client, user): tests the editing of a user with a given ID.
        - test_delete_user(client, user): tests the deletion of a user with a given ID.

    """

    def test_list_users(self, client, user):
        """
        Test retrieving a list of users.

        Args:
            - client: The test client.
            - user: The user instance.

        """

        response = client.get(f"/users/?search={user.username}")
        assert response.status_code == 200
        assert b"Users" in response.data
        assert str(user.id) in response.data.decode("utf-8")

        response = client.get(f"/users/?birth_date={user.birth_date}-{user.birth_date}")
        assert response.status_code == 200
        assert b"Users" in response.data
        assert str(user.id) in response.data.decode("utf-8")

        response = client.get(
            f"/users/?date_created={user.date_created}-{user.date_created}"
        )
        assert response.status_code == 200
        assert b"Users" in response.data
        assert str(user.id) in response.data.decode("utf-8")

        response = client.get(
            f"/users/?date_modified={user.date_modified}-{user.date_modified}"
        )
        assert response.status_code == 200
        assert b"Users" in response.data
        assert str(user.id) in response.data.decode("utf-8")

        response = client.get("/users/")
        assert response.status_code == 200
        assert b"Users" in response.data
        assert str(user.id) in response.data.decode("utf-8")
        assert user.username in response.data.decode("utf-8")
        assert user.email in response.data.decode("utf-8")
        assert user.phone in response.data.decode("utf-8")
        assert user.first_name in response.data.decode("utf-8")
        assert user.last_name in response.data.decode("utf-8")
        assert user.birth_date.strftime("%Y-%m-%d") in response.data.decode("utf-8")
        assert datetime.strftime(datetime.utcnow(), "%Y-%m-%d") in response.data.decode(
            "utf-8"
        )
        assert User.query.count() == 1

    def test_get_user(self, client, user):
        """
        Test retrieving a user with a given ID.

        Args:
            - client: The test client.
            - user: The user instance.

        """

        response = client.get("/users/1")
        assert response.status_code == 200
        assert str(user.id) in response.data.decode("utf-8")
        assert user.username in response.data.decode("utf-8")
        assert user.email in response.data.decode("utf-8")
        assert user.phone in response.data.decode("utf-8")
        assert user.first_name in response.data.decode("utf-8")
        assert user.last_name in response.data.decode("utf-8")
        assert datetime.strftime(user.birth_date, "%Y-%m-%d") in response.data.decode(
            "utf-8"
        )
        assert datetime.strftime(datetime.utcnow(), "%Y-%m-%d") in response.data.decode(
            "utf-8"
        )

    def test_get_nonexistent_user(self, client):
        """
        Test retrieving a user that does not exist.

        Args:
            - client: The test client.
            - user: The user instance.

        """

        response = client.get("/users/9999", data={})
        assert response.status_code == 404

    def test_create_user(self, client):
        """
        Test creating a new user.

        Args:
            - client: The test client.

        """

        data = {
            "email": fake.email(),
            "phone": fake_phone_number(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }

        response = client.post("users/0", data=data)
        assert "This field is required." in response.data.decode("utf-8")

        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": fake_phone_number(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.post("/users/0", data=data, follow_redirects=True)
        assert response.status_code == 200
        assert data["username"] in response.data.decode("utf-8")
        assert data["email"] in response.data.decode("utf-8")
        assert data["phone"] in response.data.decode("utf-8")
        assert data["first_name"] in response.data.decode("utf-8")
        assert data["last_name"] in response.data.decode("utf-8")
        assert datetime.strftime(
            data["birth_date"], "%Y-%m-%d"
        ) in response.data.decode("utf-8")
        assert datetime.strftime(datetime.utcnow(), "%Y-%m-%d") in response.data.decode(
            "utf-8"
        )
        assert User.query.filter_by(username=data["username"]).first() is not None

    def test_edit_user(self, client, user):
        """
        Test updating a user with a given ID.

        Args:
            - client: The test client.
            - user: The user instance.

        """

        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": fake_phone_number(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.put(f"/users/{user.id}", data=data)
        assert response.status_code == 200
        assert data["username"] in response.data.decode("utf-8")
        assert data["email"] in response.data.decode("utf-8")
        assert data["phone"] in response.data.decode("utf-8")
        assert data["first_name"] in response.data.decode("utf-8")
        assert data["last_name"] in response.data.decode("utf-8")
        assert datetime.strftime(
            data["birth_date"], "%Y-%m-%d"
        ) in response.data.decode("utf-8")
        assert User.query.filter_by(id=user.id).count() == 1

    def test_delete_user(self, client, user):
        """
        Test deleting a user with a given ID.

        Args:
            - client: The test client.
            - user: The user instance.

        """

        count_before = User.query.count()
        response = client.delete(f"/users/{user.id}")
        assert response.status_code == 200
        count_after = User.query.count()
        assert count_before == count_after
        assert User.query.filter_by(is_active=True).count() == count_before - 1

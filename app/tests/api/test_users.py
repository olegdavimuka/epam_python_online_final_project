"""
This module contains the tests for the users API.

Dependencies:
    - datetime
    - faker
    - app.models.users
    - app.tests.fixtures
    - app.utils.validation

Classes:
    - TestUsersAPI: A class that contains the tests for the users API.

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


class TestUsersAPI:
    """
    This class contains the tests for the users API.

    Methods:
        - test_get_users(client, user): tests the retrieval of all users.
        - test_get_user(client, user): tests the retrieval of a user with a given ID.
        - test_get_nonexistent_user(client): tests the retrieval of a nonexistent user.
        - test_delete_user(client, user): tests the deletion of a user with a given ID.
        - test_delete_nonexistent_user(client): tests the deletion of a nonexistent user.
        - test_post_user(client): tests the creation of a new user.
        - test_post_user_with_existing_username(client, user): tests the creation of a user
        with an existing username.
        - test_post_user_with_existing_email(client, user): tests the creation of a user
        with an existing email.
        - test_post_user_with_existing_phone(client, user): tests the creation of a user
        with an existing phone number.
        - test_post_user_with_invalid_phone(client): tests the creation of a user
        with an invalid phone number.
        - test_put_user_with_invalid_email(client): tests the creation of a user
        with an invalid email.
        - test_post_user_with_invalid_birth_date(client): tests the creation of a user
        with an invalid birth date.
        - test_put_user(client): tests the editing of a new user.
        - test_put_user_with_existing_username(client, user): tests the editing of a user
        with an existing username.
        - test_put_user_with_existing_email(client, user): tests the editing of a user
        with an existing email.
        - test_put_user_with_existing_phone(client, user): tests the editing of a user
        with an existing phone number.
        - test_put_user_with_invalid_phone(client): tests the editing of a user
        with an invalid phone number.
        - test_put_user_with_invalid_birth_date(client): tests the editing of a user
        with an invalid birth date.

    """

    def test_get_users(self, client, user):
        """
        Test retrieving all users.

        Args:
            - client: The test client.
            - user: The user instance.

        """

        response = client.get("/api/users/")
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["username"] == user.username

    def test_get_user(self, client, user):
        """
        Test retrieving a user with a given ID.

        Args:
            - client: The test client.
            - user: The user instance.

        """

        response = client.get(f"/api/users/{user.id}")
        assert response.status_code == 200
        assert response.json["username"] == user.username

    def test_get_nonexistent_user(self, client):
        """
        Test retrieving a nonexistent user.

        Args:
            - client: The test client.

        """

        response = client.get("/api/users/0")
        assert response.status_code == 404

    def test_delete_user(self, client, user):
        """
        Test deleting a user with a given ID.

        Args:
            - client: The test client.
            - user: The user instance.

        """

        response = client.delete(f"/api/users/{user.id}")
        assert response.status_code == 204
        assert User.query.filter_by(id=user.id).count() == 1
        assert User.query.filter_by(id=user.id).first().is_active is False

    def test_delete_nonexistent_user(self, client):
        """
        Test deleting a nonexistent user.

        Args:
            - client: The test client.

        """

        response = client.delete("/api/users/0")
        assert response.status_code == 404

    def test_post_user(self, client):
        """
        Test creating a new user.

        Args:
            - client: The test client.

        """

        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": fake_phone_number(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.post("/api/users/", data=data)
        assert response.status_code == 201
        assert response.json["username"] == data["username"]
        assert response.json["email"] == data["email"]
        assert response.json["phone"] == data["phone"]
        assert response.json["first_name"] == data["first_name"]
        assert response.json["last_name"] == data["last_name"]
        assert response.json["birth_date"] == datetime.strftime(
            data["birth_date"], "%Y-%m-%d"
        )
        assert response.json["date_created"] is not None
        assert response.json["date_modified"] is not None

    def test_post_user_with_existing_username(self, client, user):
        """
        Test creating a new user with an existing username.

        Args:
            - client: The test client.
            - user: The user instance.

        """

        data = {
            "username": user.username,
            "email": fake.email(),
            "phone": fake_phone_number(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.post("/api/users/", data=data)
        assert response.status_code == 400
        assert User.query.filter_by(username=data["username"]).count() == 1

    def test_post_user_with_existing_email(self, client, user):
        """
        Test creating a new user with an existing email.

        Args:
            - client: The test client.
            - user: The user instance.

        """

        data = {
            "username": fake.user_name(),
            "email": user.email,
            "phone": fake_phone_number(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.post("/api/users/", data=data)
        assert response.status_code == 400
        assert User.query.filter_by(email=data["email"]).count() == 1

    def test_post_user_with_existing_phone(self, client, user):
        """
        Test creating a new user with an existing phone.

        Args:
            - client: The test client.
            - user: The user instance.

        """

        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": user.phone,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.post("/api/users/", data=data)
        assert response.status_code == 400
        assert User.query.filter_by(phone=data["phone"]).count() == 1

    def test_post_user_with_invalid_phone(self, client):
        """
        Test creating a new user with an invalid phone.

        Args:
            - client: The test client.
        """

        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": "invalid",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.post("/api/users/", data=data)
        assert response.status_code == 400
        assert User.query.filter_by(phone=data["phone"]).count() == 0

    def test_post_user_with_invalid_birth_date(self, client):
        """
        Test creating a new user with an invalid birth date.

        Args:
            - client: The test client.
        """

        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": fake_phone_number(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": "invalid",
        }
        response = client.post("/api/users/", data=data)
        assert response.status_code == 400
        assert User.query.filter_by(birth_date=data["birth_date"]).count() == 0

    def test_put_user(self, client, user):
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
        response = client.put(f"/api/users/{user.id}", data=data)
        assert response.status_code == 201
        assert response.json["username"] == data["username"]
        assert response.json["email"] == data["email"]
        assert response.json["phone"] == data["phone"]
        assert response.json["first_name"] == data["first_name"]
        assert response.json["last_name"] == data["last_name"]
        assert response.json["birth_date"] == datetime.strftime(
            data["birth_date"], "%Y-%m-%d"
        )
        assert User.query.filter_by(id=user.id).count() == 1

    def test_put_user_with_existing_username(self, client, user):
        """
        Test updating a user with an existing username.

        Args:
            - client: The test client.
            - user: The user instance.

        """

        data = {
            "username": user.username,
            "email": fake.email(),
            "phone": fake_phone_number(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.put(f"/api/users/{user.id}", data=data)
        assert response.status_code == 400
        assert User.query.filter_by(username=data["username"]).count() == 1

    def test_put_user_with_existing_email(self, client, user):
        """
        Test updating a user with an existing email.

        Args:
            - client: The test client.
            - user: The user instance.

        """

        data = {
            "username": fake.user_name(),
            "email": user.email,
            "phone": fake_phone_number(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.put(f"/api/users/{user.id}", data=data)
        assert response.status_code == 400
        assert User.query.filter_by(email=data["email"]).count() == 1

    def test_put_user_with_existing_phone(self, client, user):
        """
        Test updating a user with an existing phone.

        Args:
            - client: The test client.
            - user: The user instance.

        """

        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": user.phone,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.put(f"/api/users/{user.id}", data=data)
        assert response.status_code == 400
        assert User.query.filter_by(phone=data["phone"]).count() == 1

    def test_put_user_with_invalid_email(self, client, user):
        """
        Test updating a user with an invalid email.

        Args:
            - client: The test client.
            - user: The user instance.

        """

        data = {
            "username": fake.user_name(),
            "email": "invalid",
            "phone": fake_phone_number(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.put(f"/api/users/{user.id}", data=data)
        assert response.status_code == 400
        assert User.query.filter_by(phone=data["email"]).count() == 0

    def test_put_user_with_invalid_phone(self, client, user):
        """
        Test updating a user with an invalid phone.

        Args:
            - client: The test client.
            - user: The user instance.

        """

        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": "invalid",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.put(f"/api/users/{user.id}", data=data)
        assert response.status_code == 400
        assert User.query.filter_by(phone=data["phone"]).count() == 0

    def test_put_user_with_invalid_birth_date(self, client, user):
        """
        Test updating a user with an invalid birth date.

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
            "birth_date": "invalid",
        }
        response = client.put(f"/api/users/{user.id}", data=data)
        assert response.status_code == 400
        assert User.query.filter_by(birth_date=data["birth_date"]).count() == 0

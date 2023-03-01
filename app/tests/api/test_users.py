from datetime import datetime

import pytest
from faker import Faker

from app import create_app, db
from app.config import TestingConfig
from app.models.users import User
from app.utils.validation import fake_phone_number

fake = Faker()


@pytest.fixture()
def app():
    """
    Create and configure a new app instance for each test.
    """

    app = create_app(config_class=TestingConfig)

    with app.app_context():
        db.create_all()
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            phone=fake_phone_number(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            birth_date=fake.date_of_birth(),
        )
        db.session.add(user)
        db.session.commit()

        yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    A test client for the app.
    """

    with app.test_client() as client:
        yield client


@pytest.fixture
def runner(app):
    """
    A test runner for the app's Click commands.
    """

    return app.test_cli_runner()


@pytest.fixture
def user(app):
    """
    A user for the tests.
    """

    with app.app_context():
        user = User.query.first()
        yield user


class TestUsersAPI:
    """
    Test users API.
    """

    def test_get_users(self, client, user):
        """
        Test retrieving all users.
        """

        response = client.get("/api/users")
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["username"] == user.username

    def test_get_user(self, client, user):
        """
        Test retrieving a user with a given ID.
        """

        response = client.get(f"/api/users/{user.id}")
        assert response.status_code == 200
        assert response.json["username"] == user.username

    def test_get_nonexistent_user(self, client):
        """
        Test retrieving a nonexistent user.
        """

        response = client.get("/api/users/0")
        assert response.status_code == 404

    def test_delete_user(self, client, user):
        """
        Test deleting a user with a given ID.
        """

        response = client.delete(f"/api/users/{user.id}")
        assert response.status_code == 204
        assert User.query.filter_by(id=user.id).count() == 0

    def test_delete_nonexistent_user(self, client):
        """
        Test deleting a nonexistent user.
        """

        response = client.delete("/api/users/0")
        assert response.status_code == 404

    def test_post_user(self, client):
        """
        Test creating a new user.
        """

        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": "+380000000001",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.post("/api/users", data=data)
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
        """

        data = {
            "username": user.username,
            "email": fake.email(),
            "phone": "+380000000001",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.post("/api/users", data=data)
        assert response.status_code == 400
        assert User.query.filter_by(username=data["username"]).count() == 1

    def test_post_user_with_existing_email(self, client, user):
        """
        Test creating a new user with an existing email.
        """

        data = {
            "username": fake.user_name(),
            "email": user.email,
            "phone": "+380000000001",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.post("/api/users", data=data)
        assert response.status_code == 400
        assert User.query.filter_by(email=data["email"]).count() == 1

    def test_post_user_with_existing_phone(self, client, user):
        """
        Test creating a new user with an existing phone.
        """

        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": user.phone,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.post("/api/users", data=data)
        assert response.status_code == 400
        assert User.query.filter_by(phone=data["phone"]).count() == 1

    def test_post_user_with_invalid_phone(self, client):
        """
        Test creating a new user with an invalid phone.
        """

        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": "invalid",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.post("/api/users", data=data)
        assert response.status_code == 400
        assert User.query.filter_by(phone=data["phone"]).count() == 0

    def test_post_user_with_invalid_birth_date(self, client):
        """
        Test creating a new user with an invalid birth date.
        """

        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": "+380000000001",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": "invalid",
        }
        response = client.post("/api/users", data=data)
        assert response.status_code == 400
        assert User.query.filter_by(birth_date=data["birth_date"]).count() == 0

    def test_put_user(self, client, user):
        """
        Test updating a user with a given ID.
        """

        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": "+380000000001",
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
        """

        data = {
            "username": user.username,
            "email": fake.email(),
            "phone": "+380000000001",
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
        """

        data = {
            "username": fake.user_name(),
            "email": user.email,
            "phone": "+380000000001",
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

    def test_put_user_with_invalid_phone(self, client, user):
        """
        Test updating a user with an invalid phone.
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
        """

        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": "+380000000001",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": "invalid",
        }
        response = client.put(f"/api/users/{user.id}", data=data)
        assert response.status_code == 400
        assert User.query.filter_by(birth_date=data["birth_date"]).count() == 0

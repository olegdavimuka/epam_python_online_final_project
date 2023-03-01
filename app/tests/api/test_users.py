from datetime import datetime

import pytest
from faker import Faker

from app import create_app, db
from app.config import TestingConfig
from app.models.users import User

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
            username="test",
            email="test@gmail.com",
            phone="+380000000000",
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

    def test_get_users(self, client):
        """
        Test retrieving all users.
        """

        response = client.get("/api/users")
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["username"] == User.query.first().username

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

        response = client.get("/api/users/999")
        assert response.status_code == 404

    def test_post_user(self, client):
        """
        Test creating a new user.
        """

        new_user_data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": "+380000000001",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.post("/api/users", data=new_user_data)
        assert response.status_code == 201
        assert response.json["username"] == new_user_data["username"]
        assert response.json["email"] == new_user_data["email"]
        assert response.json["phone"] == new_user_data["phone"]
        assert response.json["first_name"] == new_user_data["first_name"]
        assert response.json["last_name"] == new_user_data["last_name"]
        assert response.json["birth_date"] == datetime.strftime(
            new_user_data["birth_date"], "%Y-%m-%d"
        )
        assert response.json["date_created"] is not None
        assert response.json["date_modified"] is not None

    def test_post_user_with_existing_username(self, client, user):
        """
        Test creating a new user with an existing username.
        """

        user_data = {
            "username": user.username,
            "email": fake.email(),
            "phone": "+380000000001",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.post("/api/users", data=user_data)
        assert response.status_code == 400
        assert User.query.filter_by(username=user_data["username"]).count() == 1

    def test_post_user_with_existing_email(self, client, user):
        """
        Test creating a new user with an existing email.
        """

        user_data = {
            "username": fake.user_name(),
            "email": user.email,
            "phone": "+380000000001",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.post("/api/users", data=user_data)
        assert response.status_code == 400
        assert User.query.filter_by(email=user_data["email"]).count() == 1

    def test_post_user_with_existing_phone(self, client, user):
        """
        Test creating a new user with an existing phone.
        """

        user_data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": user.phone,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.post("/api/users", data=user_data)
        assert response.status_code == 400
        assert User.query.filter_by(phone=user_data["phone"]).count() == 1

    def test_post_user_with_invalid_phone(self, client):
        """
        Test creating a new user with an invalid phone.
        """

        new_user_data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": "invalid",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.post("/api/users", data=new_user_data)
        assert response.status_code == 400
        assert User.query.filter_by(phone=new_user_data["phone"]).count() == 0

    def test_post_user_with_invalid_birth_date(self, client):
        """
        Test creating a new user with an invalid birth date.
        """

        new_user_data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": "+380000000001",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": "invalid",
        }
        response = client.post("/api/users", data=new_user_data)
        assert response.status_code == 400
        assert User.query.filter_by(birth_date=new_user_data["birth_date"]).count() == 0

    def test_delete_user(self, client, user):
        """
        Test deleting a user with a given ID.
        """

        response = client.delete(f"/api/users/{user.id}")
        assert response.status_code == 204
        assert User.query.filter_by(id=user.id).count() == 0

    def test_put_user(self, client, user):
        """
        Test updating a user with a given ID.
        """

        new_user_data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": "+380000000001",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.put(f"/api/users/{user.id}", data=new_user_data)
        assert response.status_code == 201
        assert response.json["username"] == new_user_data["username"]
        assert response.json["email"] == new_user_data["email"]
        assert response.json["phone"] == new_user_data["phone"]
        assert response.json["first_name"] == new_user_data["first_name"]
        assert response.json["last_name"] == new_user_data["last_name"]
        assert response.json["birth_date"] == datetime.strftime(
            new_user_data["birth_date"], "%Y-%m-%d"
        )
        assert User.query.filter_by(id=user.id).count() == 1

    def test_put_user_with_existing_username(self, client, user):
        """
        Test updating a user with an existing username.
        """

        new_user_data = {
            "username": user.username,
            "email": fake.email(),
            "phone": "+380000000001",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.put(f"/api/users/{user.id}", data=new_user_data)
        assert response.status_code == 400
        assert User.query.filter_by(username=new_user_data["username"]).count() == 1

    def test_put_user_with_existing_email(self, client, user):
        """
        Test updating a user with an existing email.
        """

        new_user_data = {
            "username": fake.user_name(),
            "email": user.email,
            "phone": "+380000000001",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.put(f"/api/users/{user.id}", data=new_user_data)
        assert response.status_code == 400
        assert User.query.filter_by(email=new_user_data["email"]).count() == 1

    def test_put_user_with_existing_phone(self, client, user):
        """
        Test updating a user with an existing phone.
        """

        new_user_data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": user.phone,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.put(f"/api/users/{user.id}", data=new_user_data)
        assert response.status_code == 400
        assert User.query.filter_by(phone=new_user_data["phone"]).count() == 1

    def test_put_user_with_invalid_phone(self, client, user):
        """
        Test updating a user with an invalid phone.
        """

        new_user_data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": "invalid",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(),
        }
        response = client.put(f"/api/users/{user.id}", data=new_user_data)
        assert response.status_code == 400
        assert User.query.filter_by(phone=new_user_data["phone"]).count() == 0

    def test_put_user_with_invalid_birth_date(self, client, user):
        """
        Test updating a user with an invalid birth date.
        """

        new_user_data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": "+380000000001",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": "invalid",
        }
        response = client.put(f"/api/users/{user.id}", data=new_user_data)
        assert response.status_code == 400
        assert User.query.filter_by(birth_date=new_user_data["birth_date"]).count() == 0

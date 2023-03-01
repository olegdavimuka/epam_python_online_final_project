import pytest
from faker import Faker

from app import create_app, db
from app.config import TestingConfig
from app.constants.currency import Currency
from app.models.purses import Purse
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

        purse = Purse(user_id=user.id, currency=Currency.USD.value)
        db.session.add(purse)
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


@pytest.fixture
def purse(app):
    """
    A purse for the tests.
    """

    with app.app_context():
        purse = Purse.query.first()
        yield purse


class TestPursesAPI:
    """
    Test purses API.
    """

    def test_get_purses(self, client, purse):
        """
        Test retrieving all purses.
        """

        response = client.get("/api/purses")
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["id"] == purse.id
        assert response.json[0]["user_id"] == purse.user_id
        assert response.json[0]["currency"] == Currency(purse.currency).value
        assert response.json[0]["balance"] == purse.balance

    def test_get_purse(self, client, purse):
        """
        Test retrieving a purse with a given ID.
        """

        response = client.get(f"/api/purses/{purse.id}")
        assert response.status_code == 200
        assert response.json["id"] == purse.id
        assert response.json["user_id"] == purse.user_id
        assert response.json["currency"] == Currency(purse.currency).value
        assert response.json["balance"] == purse.balance

    def test_get_nonexistent_purse(self, client):
        """
        Test retrieving a nonexistent user.
        """

        response = client.get("/api/purses/0")
        assert response.status_code == 404

    def test_delete_purse(self, client, purse):
        """
        Test deleting a purse with a given ID.
        """

        response = client.delete(f"/api/purses/{purse.id}")
        assert response.status_code == 204
        assert Purse.query.filter_by(id=purse.id).count() == 0

    def test_delete_nonexistent_purse(self, client):
        """
        Test deleting a nonexistent purse.
        """

        response = client.delete("/api/purses/0")
        assert response.status_code == 404

    def test_post_purse(self, client, user):
        """
        Test creating a new purse.
        """

        data = {
            "user_id": user.id,
            "currency": Currency.USD.value,
        }

        response = client.post("/api/purses", data=data)
        assert response.status_code == 201
        assert response.json["user_id"] == user.id
        assert response.json["currency"] == Currency.USD.value
        assert response.json["balance"] == 0.0

    def test_create_purse_with_invalid_user_id(self, client):
        """
        Test creating a purse with an invalid user id.
        """

        data = {
            "user_id": 0,
            "currency": Currency.USD,
        }

        response = client.post("/api/purses", data=data)
        assert response.status_code == 400

    def test_create_purse_with_invalid_currency(self, client, user):
        """
        Test creating a purse with an invalid currency.
        """

        data = {
            "user_id": user.id,
            "currency": "invalid",
        }

        response = client.post("/api/purses", data=data)
        assert response.status_code == 400

import pytest
from faker import Faker

from app import create_app, db
from app.config import TestingConfig
from app.constants.currency import Currency
from app.models.purses import Purse
from app.models.transactions import Transaction
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

        purse1 = Purse(user_id=user.id, currency=Currency.USD.value, balance=1000)
        purse2 = Purse(user_id=user.id, currency=Currency.EUR.value, balance=1000)
        db.session.add(purse1)
        db.session.add(purse2)
        db.session.commit()

        transaction = Transaction(
            purse_from_id=purse1.id,
            purse_to_id=purse2.id,
            purse_from_amount=100,
        )

        db.session.add(transaction)
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


@pytest.fixture
def purses(app):
    """
    A list of purses for the tests.
    """

    with app.app_context():
        purses = Purse.query.all()
        yield purses


@pytest.fixture
def transaction(app):
    """
    A transaction for the tests.
    """

    with app.app_context():
        transaction = Transaction.query.first()
        yield transaction


class TestTransactionsAPI:
    """
    Test transactions API.
    """

    def test_get_transactions(self, client, transaction):
        """
        Test retrieving all transactions.
        """

        response = client.get("/api/transactions")
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["id"] == transaction.id
        assert response.json[0]["purse_from_id"] == transaction.purse_from_id
        assert response.json[0]["purse_to_id"] == transaction.purse_to_id
        assert (
            response.json[0]["purse_from_currency"]
            == Currency(transaction.purse_from_currency).value
        )
        assert (
            response.json[0]["purse_to_currency"]
            == Currency(transaction.purse_to_currency).value
        )
        assert response.json[0]["purse_from_amount"] == transaction.purse_from_amount
        assert response.json[0]["purse_to_amount"] == transaction.purse_to_amount

    def test_get_transaction(self, client, transaction):
        """
        Test retrieving a transaction with a given ID.
        """

        response = client.get(f"/api/transactions/{transaction.id}")
        assert response.status_code == 200
        assert response.json["id"] == transaction.id
        assert response.json["purse_from_id"] == transaction.purse_from_id
        assert response.json["purse_to_id"] == transaction.purse_to_id
        assert (
            response.json["purse_from_currency"]
            == Currency(transaction.purse_from_currency).value
        )
        assert (
            response.json["purse_to_currency"]
            == Currency(transaction.purse_to_currency).value
        )
        assert response.json["purse_from_amount"] == transaction.purse_from_amount
        assert response.json["purse_to_amount"] == transaction.purse_to_amount

    def test_get_nonexistent_transaction(self, client):
        """
        Test retrieving a nonexistent transaction.
        """

        response = client.get("/api/transactions/0")
        assert response.status_code == 404

    def test_post_transaction(self, client, purses):
        """
        Test creating a new transaction.

        Before:
            - purse1: 900 USD
            - purse2: 1095 EUR

        Exchange rate:
            - USD/EUR: 0.95

        After:
            - purse1: 800 USD (100 USD was sent to purse2)
            - purse2: 1190 EUR (95 EUR was received from purse1)
        """

        data = {
            "purse_from_id": purses[0].id,
            "purse_to_id": purses[1].id,
            "purse_from_amount": 100,
        }

        response = client.post("/api/transactions", data=data)
        assert response.status_code == 201
        assert response.json["purse_from_id"] == purses[0].id
        assert response.json["purse_to_id"] == purses[1].id
        assert (
            response.json["purse_from_currency"] == Currency(purses[0].currency).value
        )
        assert response.json["purse_to_currency"] == Currency(purses[1].currency).value
        assert response.json["purse_from_amount"] == 100
        assert response.json["purse_to_amount"] == 95  # 100 * 0.95

        assert purses[0].balance == 800
        assert purses[1].balance == 1190

    def test_post_transaction_invalid_purse_from(self, client, purse):
        """
        Test creating a new transaction with an invalid purse.
        """

        data = {
            "purse_from_id": 0,
            "purse_to_id": purse.id,
            "purse_from_amount": 100,
        }

        response = client.post("/api/transactions", data=data)
        assert response.status_code == 400

    def test_post_transaction_invalid_purse_to(self, client, purse):
        """
        Test creating a new transaction with an invalid purse.
        """

        data = {
            "purse_from_id": purse.id,
            "purse_to_id": 0,
            "purse_from_amount": 100,
        }

        response = client.post("/api/transactions", data=data)
        assert response.status_code == 400

    def test_post_transaction_not_enough_funds(self, client, purses):
        """
        Test creating a new transaction with not enough funds.
        """

        data = {
            "purse_from_id": purses[0].id,
            "purse_to_id": purses[1].id,
            "purse_from_amount": 10000,
        }

        response = client.post("/api/transactions", data=data)
        assert response.status_code == 400

    def test_post_transaction_same_purse(self, client, purse):
        """
        Test creating a new transaction with the same purse.
        """

        data = {
            "purse_from_id": purse.id,
            "purse_to_id": purse.id,
            "purse_from_amount": 100,
        }

        response = client.post("/api/transactions", data=data)
        assert response.status_code == 400

"""
This module contains the fixtures for the tests for the API.

Dependencies:
    - faker
    - app
    - app.config
    - app.constants.currency
    - app.models.purses
    - app.models.transactions
    - app.models.users
    - app.utils.validation

Functions:
    - fixture_app(): A fixture creates a new app instance for each test.
    - fixture_client(app): A fixture that yields a test client for the app.
    - fixture_user(app): A fixture that yields a user for the app.
    - fixture_purse(app): A fixture that yields a purse for the app.
    - fixture_purses(app): A fixture that yields a list of purses for the app.
    - fixture_transaction(app): A fixture that yields a transaction for the app.

"""

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


@pytest.fixture(name="app")
def fixture_app():
    """
    This fixture creates a new app instance for each test, and configures it to use the
    TestingConfig configuration class. It also creates a new database session and adds a
    user and two purses to the database. The fixture yields the app instance, and then
    tears down the database session and drops all tables after the test is complete.

    Returns:
        - app: The app instance.

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
        purse3 = Purse(user_id=user.id, currency=Currency.USD.value, balance=1000)
        db.session.add(purse1)
        db.session.add(purse2)
        db.session.add(purse3)
        db.session.commit()

        transaction = Transaction()
        transaction.update(
            **{
                "purse_from_id": purse1.id,
                "purse_to_id": purse2.id,
                "purse_from_amount": 100,
            }
        )
        # Rate = 0.95:
        # purse1.balance = 1000 - 100 = 900
        # purse2.balance = 1000 + 100 * 0,95 = 1095.
        # purse3.balance = 1000

        db.session.add(transaction)
        db.session.commit()

        yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(name="client")
def fixture_client(app):
    """
    A fixture that yields a test client for the app.

    Args:
        - app: The app instance.

    Returns:
        - client: The test client.
    """

    with app.test_client() as client:
        yield client


@pytest.fixture(name="user")
def fixture_user(app):
    """
    A fixture that yields a user for the app.

    Args:
        - app: The app instance.

    Returns:
        - user: The user instance.

    """

    with app.app_context():
        user = User.query.first()
        yield user


@pytest.fixture(name="purse")
def fixture_purse(app):
    """
    A fixture that yields a purse for the app.

    Args:
        - app: The app instance.

    Returns:
        - purse: The purse instance.

    """

    with app.app_context():
        purse = Purse.query.first()
        yield purse


@pytest.fixture(name="purses")
def fixture_purses(app):
    """
    A fixture that yields a list of purses for the app.

    Args:
        - app: The app instance.

    Returns:
        - purses: The list of purses.

    """

    with app.app_context():
        purses = Purse.query.all()
        yield purses


@pytest.fixture(name="transaction")
def fixture_transaction(app):
    """
    A fixture that yields a transaction for the app.

    Args:
        - app: The app instance.

    Returns:
        - transaction: The transaction instance.

    """

    with app.app_context():
        transaction = Transaction.query.first()
        yield transaction

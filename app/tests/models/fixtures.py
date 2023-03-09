"""
This module contains the fixtures for the tests for the models module.

Dependencies:
    - datetime
    - pytest
    - app
    - app.constants.currency
    - app.models.purses
    - app.models.transactions
    - app.models.users

Functions:
    - user(): A fixture that yields a user for the app.
    - client(app): A fixture that yields a test client for the app.
    - purse(app): A fixture that yields a purse for the app.
    - transaction(app): A fixture that yields a transaction for the app.

"""

from datetime import datetime

import pytest

from app import create_app, db
from app.constants.currency import Currency
from app.models.purses import Purse
from app.models.transactions import Transaction
from app.models.users import User


@pytest.fixture(name="user")
def fixture_user():
    """
    This fixture yields a user for the app.

    Returns:
        - user: A user for the app.

    """

    user = User(
        username="testuser",
        email="testuser@example.com",
        phone="123-456-7890",
        first_name="John",
        last_name="Doe",
        birth_date=datetime(2000, 1, 1).date(),
        date_created=datetime(2020, 1, 1),
        date_modified=datetime(2020, 1, 1),
    )
    return user


@pytest.fixture(name="client")
def fixture_client():
    """
    This fixture yields a test client for the app.

    Returns:
        - testing_client: A test client for the app.

    """

    flask_app = create_app("testing")
    testing_client = flask_app.test_client()
    with flask_app.app_context():
        db.create_all()
        yield testing_client
        db.session.remove()
        db.drop_all()


@pytest.fixture(name="purse")
def fixture_purse():
    """
    This fixture yields a purse for the app.

    Returns:
        - purse: A purse for the app.

    """

    return Purse(
        user_id=1,
        currency=Currency.USD,
        balance=100.0,
        date_created=datetime(2022, 3, 8, 12, 0, 0),
        date_modified=datetime(2022, 3, 8, 12, 0, 0),
        is_active=True,
    )


@pytest.fixture(name="transaction")
def fixture_transaction():
    """
    This fixture yields a transaction for the app.

    Returns:
        - transaction: A transaction for the app.

    """

    return Transaction(
        purse_from_id=1,
        purse_to_id=2,
        purse_from_currency=Currency.USD,
        purse_to_currency=Currency.EUR,
        purse_from_amount=100.0,
        purse_to_amount=95.0,
        date_created=datetime(2022, 3, 8, 12, 0, 0),
    )

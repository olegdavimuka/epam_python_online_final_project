"""
This module populates a database with fake data for testing and development purposes.

Dependencies:
    - datetime
    - random
    - Faker
    - app.constants.currency
    - app.models.purses
    - app.models.transactions
    - app.models.users

Functions:
    - _create_fake_users(db): creates and saves fake users to the database.
    - _create_fake_purses(db): creates and saves fake purses to the database.
    - _create_fake_transactions(db): creates and saves fake transactions to the database.
    - populate_db(db): populates the database with fake data by calling the above three functions.

"""

from datetime import datetime
from random import randint

from faker import Faker

from app.constants.currency import Currency
from app.models.purses import Purse
from app.models.transactions import Transaction
from app.models.users import User

fake = Faker()


def _create_fake_users(_db):
    """
    Create and save fake users to the database.

    Args:
        - _db (SQLAlchemy): database object.

    """

    users = []
    phone = "+380000000000"
    for _ in range(9):
        phone = phone[:-1] + str(int(phone[-1]) + 1)
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            phone=phone,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            birth_date=fake.date_of_birth(),
            date_created=datetime.now(),
            date_modified=datetime.now(),
        )
        users.append(user)
    _db.session.add_all(users)
    _db.session.commit()


def _create_fake_purses(_db):
    """
    Create and save fake purses to the database.

    Args:
        - _db (SQLAlchemy): database object.

    """

    purses = []
    users = User.query.all()
    for user in users:
        for currency in Currency:
            purse = Purse(
                user_id=user.id,
                currency=currency.value,
                balance=randint(0, 1000),
                date_created=datetime.now(),
                date_modified=datetime.now(),
            )
            purses.append(purse)
    _db.session.add_all(purses)
    _db.session.commit()


def _create_fake_transactions(_db):
    """
    Create and save fake transactions to the database.

    Args:
        - _db (SQLAlchemy): database object.

    """

    transactions = []
    for _ in range(100):
        purse_from = Purse.query.order_by(_db.func.random()).first()
        purse_to = (
            Purse.query.filter(
                Purse.user_id != purse_from.user_id,
                Purse.currency == purse_from.currency,
            )
            .order_by(_db.func.random())
            .first()
        )
        amount = randint(0, purse_from.balance)
        transaction = Transaction(
            purse_from_id=purse_from.id,
            purse_to_id=purse_to.id,
            purse_from_currency=purse_from.currency,
            purse_to_currency=purse_to.currency,
            purse_from_amount=amount,
            purse_to_amount=amount,
            date_created=datetime.now(),
        )
        transactions.append(transaction)
    _db.session.add_all(transactions)
    _db.session.commit()


def populate_db(_db):
    """
    Populate the database with fake data.

    Args:
        - _db (SQLAlchemy): database object.

    """

    _create_fake_users(_db)
    _create_fake_purses(_db)
    _create_fake_transactions(_db)

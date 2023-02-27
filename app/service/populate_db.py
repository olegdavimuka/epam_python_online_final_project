from datetime import datetime
from random import randint

from faker import Faker

from app.constants.currency import Currency
from app.models.purses import Purse
from app.models.transactions import Transaction
from app.models.users import User

fake = Faker()


def create_fake_users(db):
    """Create and save fake users to the database."""

    users = []
    for _ in range(10):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            phone=fake.phone_number(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            birth_date=fake.date_of_birth(),
            date_created=datetime.now(),
            date_modified=datetime.now(),
        )
        users.append(user)
    db.session.add_all(users)
    db.session.commit()


def create_fake_purses(db):
    """Create and save fake purses to the database."""

    purses = []
    users = User.query.all()
    for user in users:
        for currency in Currency:
            purse = Purse(
                user_id=user.id,
                currency=currency,
                balance=randint(0, 1000),
                date_created=datetime.now(),
                date_modified=datetime.now(),
            )
            purses.append(purse)
    db.session.add_all(purses)
    db.session.commit()


def create_fake_transactions(db):
    """Create and save fake transactions to the database."""

    transactions = []
    for _ in range(10):
        purse_from = Purse.query.order_by(db.func.random()).first()
        purse_to = (
            Purse.query.filter(
                Purse.user_id != purse_from.user_id,
                Purse.currency == purse_from.currency,
            )
            .order_by(db.func.random())
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
    db.session.add_all(transactions)
    db.session.commit()

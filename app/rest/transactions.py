"""
This module defines a Flask-RESTful API for working with transaction resources.
A transaction is an object that represents the transaction between two purses,
containing an amount of money transferred. The API provides endpoints for
retrieving a single transaction, retrieving a list of all transactions
and creating a new transaction.

Dependencies:
    - logging
    - flask_restful
    - app.db
    - app.models.purses
    - app.models.transactions

Exported classes:
    - TransactionsAPI
    - TransactionsListAPI

Functions:
    - _get_transaction_or_abort_if_doesnt_exist: Retrieves a transaction with the given id
    from the database or aborts the request with a 404 error if it doesn't exist.
    - _validate_args: Validates the arguments of a request.

"""

import logging

from flask_restful import Resource, abort, reqparse

from app import db
from app.models.purses import Purse
from app.models.transactions import Transaction


def _get_transaction_or_abort_if_doesnt_exist(_id):
    """
    Retrieves a transaction with the given _id from the database or aborts the request
    with a 404 error if it doesn't exist.

    Args:
        - _id (int): The _id of the transaction to retrieve.

    Returns:
        - transaction (Transaction): The transaction object with the given _id.

    Raises:
        - 404 error: If the transaction with the given _id doesn't exist in the database.

    """

    transaction = db.session.get(Transaction, _id)
    if not transaction:
        logging.error("Transaction %s doesn't exist.", _id)
        abort(404, message=f"Transaction {_id} doesn't exist.")
    return transaction


def _validate_args(args):
    """
    Validates the arguments of a request.

    Args:
        - args (dict): The arguments of the request.

    Returns:
        - True if the arguments are valid, False otherwise.

    """

    if (
        Purse.query.filter_by(id=args["purse_from_id"]).first() is None
        or not Purse.query.filter_by(id=args["purse_from_id"]).first().is_active
    ):
        logging.error("Purse %s doesn't exist.", args["purse_from_id"])
        abort(400, message=f"Purse {args['purse_from_id']} doesn't exist.")

    if (
        Purse.query.filter_by(id=args["purse_to_id"]).first() is None
        or not Purse.query.filter_by(id=args["purse_to_id"]).first().is_active
    ):
        logging.error("Purse %s doesn't exist.", args["purse_to_id"])
        abort(400, message=f"Purse {args['purse_to_id']} doesn't exist.")

    if (
        Purse.query.filter_by(id=args["purse_from_id"]).first()
        == Purse.query.filter_by(id=args["purse_to_id"]).first()
    ):
        logging.error(
            "Purse %s and purse %s are the same.",
            args["purse_from_id"],
            args["purse_to_id"],
        )
        abort(
            400,
            message=f"Purse {args['purse_from_id']} and purse {args['purse_to_id']} are the same.",
        )

    if (
        Purse.query.filter_by(id=args["purse_from_id"]).first().balance
        < args["purse_from_amount"]
    ):
        logging.error("Purse %s doesn't have enough money.", args["purse_from_id"])
        abort(400, message=f"Purse {args['purse_from_id']} doesn't have enough money.")

    return True


parser = reqparse.RequestParser()
parser.add_argument(
    "purse_from_id",
    type=int,
    location="form",
    required=True,
    help="Purse from id is required.",
)
parser.add_argument(
    "purse_to_id",
    type=int,
    location="form",
    required=True,
    help="Purse to id is required.",
)
parser.add_argument(
    "purse_from_amount",
    type=float,
    location="form",
    required=True,
    help="Purse from amount is required.",
)


class TransactionsAPI(Resource):
    """
    Resource for retrieving and deleting a transaction.

    Methods:
        - get: Retrieves the transaction with the given _id.

    """

    def get(self, _id):
        """
        Returns the JSON representation of a transaction with the given _id.

        Args:
            - _id (int): The _id of the transaction to retrieve.

        Returns:
            - transaction_dict (dict): A dictionary containing the details of the transaction.

        """

        transaction = _get_transaction_or_abort_if_doesnt_exist(_id)
        logging.info(
            "Retrieved transaction %s. Details: %s", _id, transaction.to_dict()
        )
        return transaction.to_dict()


class TransactionsListAPI(Resource):
    """
    Resource for retrieving and creating transactions.

    Methods:
        - get: Retrieves a list of all transactions in the database.
        - post: Creates a new transaction in the database using the details provided in the request.

    Attributes:
        - parser (RequestParser): Parses the arguments of a request.

    """

    def get(self):
        """
        Returns a list of all transactions in the database.

        Returns:
            - transactions_list (list): A list of dictionaries containing
        the details of all transactions.

        """

        transactions = Transaction.query.all()
        logging.info("Retrieved all transactions. Count: %s", len(transactions))
        return [transaction.to_dict() for transaction in transactions]

    def post(self):
        """
        Creates a new transaction in the database using the details provided in the request.

        Returns:
            - transaction_dict (dict): A dictionary containing the
        details of the newly created transaction.
            - 201 status code: Indicates that the resource was successfully created.

        """

        args = parser.parse_args()
        _validate_args(args)
        transaction = Transaction()
        transaction.update(**args)
        db.session.add(transaction)
        db.session.commit()
        logging.info(
            "Created transaction %s. Details: %s", transaction.id, transaction.to_dict()
        )
        return transaction.to_dict(), 201

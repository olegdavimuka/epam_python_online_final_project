import logging

from flask_restful import Resource, abort, reqparse

from app import db
from app.models.purses import Purse
from app.models.transactions import Transaction


def get_transaction_or_abort_if_doesnt_exist(id):
    """
    Retrieves a transaction with the given id from the database or aborts the request
    with a 404 error if it doesn't exist.

    Args:
    - id (int): The id of the transaction to retrieve.

    Returns:
    - transaction (Transaction): The transaction object with the given id.

    Raises:
    - 404 error: If the transaction with the given id doesn't exist in the database.
    """

    transaction = db.session.get(Transaction, id)
    if not transaction:
        logging.error(f"Transaction {id} doesn't exist.")
        abort(404, message=f"Transaction {id} doesn't exist.")
    return transaction


def _validate_args(args):
    """
    Validates the arguments of a request.

    Args:
    - args (dict): The arguments of the request.

    Returns:
    - True if the arguments are valid, False otherwise.
    """

    if Purse.query.filter_by(id=args["purse_from_id"]).first() is None:
        logging.error(f"Purse {args['purse_from_id']} doesn't exist.")
        abort(400, message=f"Purse {args['purse_from_id']} doesn't exist.")

    if Purse.query.filter_by(id=args["purse_to_id"]).first() is None:
        logging.error(f"Purse {args['purse_to_id']} doesn't exist.")
        abort(400, message=f"Purse {args['purse_to_id']} doesn't exist.")

    if (
        Purse.query.filter_by(id=args["purse_from_id"]).first()
        == Purse.query.filter_by(id=args["purse_to_id"]).first()
    ):
        logging.error(
            f"Purse {args['purse_from_id']} and purse {args['purse_to_id']} are the same."
        )
        abort(
            400,
            message=f"Purse {args['purse_from_id']} and purse {args['purse_to_id']} are the same.",
        )

    if (
        Purse.query.filter_by(id=args["purse_from_id"]).first().balance
        < args["purse_from_amount"]
    ):
        logging.error(f"Purse {args['purse_from_id']} doesn't have enough money.")
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
    def get(self, id):
        """
        Returns the JSON representation of a transaction with the given id.

        Args:
        - id (int): The id of the transaction to retrieve.

        Returns:
        - transaction_dict (dict): A dictionary containing the details of the transaction.
        """

        transaction = get_transaction_or_abort_if_doesnt_exist(id)
        logging.info(f"Retrieved transaction {id}. Details: {transaction.to_dict()}")
        return transaction.to_dict()


class TransactionsListAPI(Resource):
    def get(self):
        """
        Returns a list of all transactions in the database.

        Returns:
        - transactions_list (list): A list of dictionaries containing the details of all transactions.
        """

        transactions = Transaction.query.all()
        logging.info(f"Retrieved all transactions. Count: {len(transactions)}")
        return [transaction.to_dict() for transaction in transactions]

    def post(self):
        """
        Creates a new transaction in the database using the details provided in the request.

        Returns:
        - transaction_dict (dict): A dictionary containing the details of the newly created transaction.
        - 201 status code: Indicates that the resource was successfully created.
        """

        args = parser.parse_args()
        _validate_args(args)
        transaction = Transaction(
            purse_from_id=args["purse_from_id"],
            purse_to_id=args["purse_to_id"],
            purse_from_amount=args["purse_from_amount"],
        )
        db.session.add(transaction)
        db.session.commit()
        logging.info(f"Created new transaction. Details: {transaction.to_dict()}")
        return transaction.to_dict(), 201

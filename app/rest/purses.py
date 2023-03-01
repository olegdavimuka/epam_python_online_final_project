import logging

from flask_restful import Resource, abort, reqparse

from app import db
from app.constants.currency import Currency
from app.models.purses import Purse
from app.models.users import User


def get_purse_or_abort_if_doesnt_exist(id):
    """
    Retrieves a purse with the given id from the database or aborts the request
    with a 404 error if it doesn't exist.

    Args:
    - id (int): The id of the purse to retrieve.

    Returns:
    - purse (purse): The purse object with the given id.

    Raises:
    - 404 error: If the purse with the given id doesn't exist in the database.
    """

    purse = db.session.get(Purse, id)
    if not purse:
        logging.error(f"purse {id} doesn't exist.")
        abort(404, message=f"purse {id} doesn't exist.")
    return purse


def _validate_args(args):
    """
    Validates the arguments of a request.

    Args:
    - args (dict): The arguments of the request.

    Returns:
    - True if the arguments are valid, False otherwise.
    """

    if User.query.filter_by(id=args["user_id"]).first() is None:
        logging.error(f"User {args['user_id']} doesn't exist.")
        abort(400, message=f"User {args['user_id']} doesn't exist.")

    if args["currency"] not in Currency.__members__:
        logging.error(f"Currency {args['currency']} is not valid.")
        abort(400, message=f"Currency {args['currency']} is not valid.")

    return True


parser = reqparse.RequestParser()
parser.add_argument(
    "user_id",
    type=int,
    location="form",
    required=True,
    help="User id is required.",
)
parser.add_argument(
    "currency",
    type=str,
    location="form",
    required=True,
    help="Currency is required.",
)


class PursesAPI(Resource):
    def get(self, id):
        """
        Returns the JSON representation of a purse with the given id.

        Args:
        - id (int): The id of the purse to retrieve.

        Returns:
        - purse_dict (dict): A dictionary containing the details of the purse.
        """
        purse = get_purse_or_abort_if_doesnt_exist(id)
        logging.info(f"Retrieved purse {id}. Details: {purse.to_dict()}")
        return purse.to_dict()

    def delete(self, id):
        """
        Deletes the purse with the given id from the database.

        Args:
        - id (int): The id of the purse to delete.

        Returns:
        - 204 status code: Indicates that the purse was deleted successfully.
        """

        purse = get_purse_or_abort_if_doesnt_exist(id)
        db.session.delete(purse)
        logging.info(f"Deleted purse {id}.")
        db.session.commit()
        return "", 204


class PursesListAPI(Resource):
    def get(self):
        """
        Returns a list of all purses in the database.

        Returns:
        - purses_list (list): A list of dictionaries containing the details of each purse.
        """

        purses = Purse.query.all()
        logging.info(f"Retrieved all purses. Count: {len(purses)}.")
        return [purse.to_dict() for purse in purses]

    def post(self):
        """
        Creates a new purse in the database using the details provided in the request.

        Returns:
        - purse_dict (dict): A dictionary containing the details of the newly created purse.
        - 201 status code: Indicates that the purse was created successfully.
        """

        args = parser.parse_args()
        _validate_args(args)
        purse = Purse(user_id=args["user_id"], currency=args["currency"])
        db.session.add(purse)
        db.session.commit()
        logging.info(f"Created new purse {purse.id}. Details: {purse.to_dict()}.")
        return purse.to_dict(), 201

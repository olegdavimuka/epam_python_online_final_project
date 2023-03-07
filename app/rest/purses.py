"""
This module defines a Flask-RESTful API for working with purse resources. A purse is an object
that represents the wallet of a particular user, containing a balance in a specific currency.
The API provides endpoints for retrieving a single purse, deleting a purse, retrieving a list of
all purses, and creating a new purse.

Dependencies:
    - logging
    - flask_restful
    - app.db
    - app.constants.currency
    - app.models.users
    - app.models.purses

Exported classes:
    - PursesAPI
    - PursesListAPI

Functions:
    - _get_purse_or_abort_if_doesnt_exist: Retrieves a purse with the given id from the database or
    aborts the request with a 404 error if it doesn't exist.
    - _validate_args: Validates the arguments of a request.

"""

import logging

from flask_restful import Resource, abort, reqparse

from app import db
from app.constants.currency import Currency
from app.models.purses import Purse
from app.models.users import User


def _get_purse_or_abort_if_doesnt_exist(_id):
    """
    Retrieves a purse with the given _id from the database or aborts the request
    with a 404 error if it doesn't exist.

    Args:
        - _id (int): The _id of the purse to retrieve.

    Returns:
        - purse (purse): The purse object with the given _id.

    Raises:
        - 404 error: If the purse with the given _id doesn't exist in the database.

    """

    purse = db.session.get(Purse, _id)
    if not purse:
        logging.error("purse %s doesn't exist.", _id)
        abort(404, message=f"purse {_id} doesn't exist.")
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
        logging.error("User %s doesn't exist.", args["user_id"])
        abort(400, message=f"User {args['user_id']} doesn't exist.")

    if args["currency"] not in Currency.__members__:
        logging.error("Currency %s is not valid.", args["currency"])
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
    """
    Resource for retrieving and deleting a purse.

    Methods:
        - get: Retrieves the purse with the given _id.
        - delete: Deletes the purse with the given _id.

    """

    def get(self, _id):
        """
        Returns the JSON representation of a purse with the given _id.

        Args:
            - _id (int): The _id of the purse to retrieve.

        Returns:
            - purse_dict (dict): A dictionary containing the details of the purse.

        """
        purse = _get_purse_or_abort_if_doesnt_exist(_id)
        logging.info("Retrieved purse %s. Details: %s.", _id, purse.to_dict())
        return purse.to_dict()

    def delete(self, _id):
        """
        Deletes the purse with the given _id from the database.

        Args:
            - _id (int): The _id of the purse to delete.

        Returns:
            - 204 status code: Indicates that the purse was deleted successfully.

        """

        purse = _get_purse_or_abort_if_doesnt_exist(_id)
        purse.is_active = False
        logging.info("Deleted purse %s.", _id)
        db.session.commit()
        return "", 204


class PursesListAPI(Resource):
    """
    Resource for retrieving and creating purses.

    Methods:
        - get: Retrieves a list of all purses in the database.
        - post: Creates a new purse in the database using the details provided in the request.

    Attributes:
        - parser (RequestParser): Parses the arguments of a request.

    """

    def get(self):
        """
        Returns a list of all purses in the database.

        Returns:
            - purses_list (list): A list of dictionaries containing the details of each purse.

        """

        purses = Purse.query.all()
        logging.info("Retrieved all purses. Count: %s.", len(purses))
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
        logging.info("Created new purse %s. Details: %s.", purse.id, purse.to_dict())
        return purse.to_dict(), 201

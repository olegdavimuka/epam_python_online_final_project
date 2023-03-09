"""
This module defines a Flask-RESTful API for working with users resources. A purse is an object
that represents a particular user. The API provides endpoints for retrieving a single user,
deleting a user, updating a user, retrieving a list of all users, and creating a new user.

Dependencies:
    - logging
    - datetime
    - flask_restful
    - app.db
    - app.models.purses
    - app.models.users
    - app.utils.validation

Exported classes:
    - UsersAPI
    - UsersListAPI

Functions:
    - _get_user_or_abort_if_doesnt_exist: Retrieves a user with the given id from the database or
    aborts the request with a 404 error if it doesn't exist.
    - _validate_args: Validates the arguments of a request.

"""

import logging
from datetime import datetime

from flask_restful import Resource, abort, reqparse

from app import db
from app.models.purses import Purse
from app.models.users import User
from app.utils.validation import is_valid_date, is_valid_email, is_valid_phone_number


def _get_user_or_abort_if_doesnt_exist(_id):
    """
    Retrieves a user with the given _id from the database or aborts the request
    with a 404 error if it doesn't exist.

    Args:
        - _id (int): The _id of the user to retrieve.

    Returns:
        - user (user): The user object with the given _id.

    Raises:
        - 404 error: If the user with the given _id doesn't exist in the database.

    """

    user = db.session.get(User, _id)
    if not user or not user.is_active:
        logging.error("user %s doesn't exist.", _id)
        abort(404, message=f"user {_id} doesn't exist.")
    return user


def _validate_args(args):
    """
    Validates the arguments of a request.

    Args:
        - args (dict): The arguments of the request.

    Returns:
        - True if the arguments are valid, False otherwise.

    """

    if User.query.filter_by(username=args["username"]).first():
        logging.error("Username %s already exists.", args["username"])
        abort(400, message=f"Username {args['username']} already exists.")

    if User.query.filter_by(email=args["email"]).first():
        logging.error("Email %s already exists.", args["email"])
        abort(400, message=f"Email {args['email']} already exists.")

    if User.query.filter_by(phone=args["phone"]).first():
        logging.error("Phone %s already exists.", args["phone"])
        abort(400, message=f"Phone {args['phone']} already exists.")

    if is_valid_date(args["birth_date"]) is False:
        logging.error("Birth date %s is not valid.", args["birth_date"])
        abort(400, message=f"Birth date {args['birth_date']} is not valid.")

    if is_valid_phone_number(args["phone"]) is False:
        logging.error("Phone %s is not valid.", args["phone"])
        abort(400, message=f"Phone {args['phone']} is not valid.")

    if is_valid_email(args["email"]) is False:
        logging.error("Email %s is not valid.", args["email"])
        abort(400, message=f"Email {args['email']} is not valid.")

    return True


post_parser = reqparse.RequestParser()
post_parser.add_argument(
    "username",
    type=str,
    location="form",
    required=True,
    help="Username is required.",
)
post_parser.add_argument(
    "email",
    type=str,
    location="form",
    required=True,
    help="Email is required.",
)
post_parser.add_argument(
    "phone",
    type=str,
    location="form",
    required=True,
    help="Phone is required.",
)
post_parser.add_argument(
    "first_name",
    type=str,
    location="form",
    required=True,
    help="First name is required.",
)
post_parser.add_argument(
    "last_name",
    type=str,
    location="form",
    required=True,
    help="Last name is required.",
)
post_parser.add_argument(
    "birth_date",
    type=str,
    location="form",
    required=True,
    help="Birth date is required.",
)

put_parser = reqparse.RequestParser()
put_parser.add_argument(
    "username",
    type=str,
    location="form",
    required=False,
    help="Username is required.",
)
put_parser.add_argument(
    "email",
    type=str,
    location="form",
    required=False,
    help="Email is required.",
)
put_parser.add_argument(
    "phone",
    type=str,
    location="form",
    required=False,
    help="Phone is required.",
)
put_parser.add_argument(
    "first_name",
    type=str,
    location="form",
    required=False,
    help="First name is required.",
)
put_parser.add_argument(
    "last_name",
    type=str,
    location="form",
    required=False,
    help="Last name is required.",
)
put_parser.add_argument(
    "birth_date",
    type=str,
    location="form",
    required=False,
    help="Birth date is required.",
)


class UsersAPI(Resource):
    """
    Resource for retrieving, updating and deleting a user.

    Methods:
        - get: Retrieves the user with the given _id.
        - delete: Deletes the user with the given _id.
        - put: Updates the user with the given _id.

    """

    def get(self, _id):
        """
        Returns the JSON representation of a user with the given _id.

        Args:
            - _id (int): The _id of the user to retrieve.

        Returns:
            - user_dict (dict): A dictionary containing the details of the user.

        """

        user = _get_user_or_abort_if_doesnt_exist(_id)
        logging.info("Retrieved user %s. Details: %s.", _id, user.to_dict())
        return user.to_dict()

    def delete(self, _id):
        """
        Deletes the user with the given _id from the database.

        Args:
            - _id (int): The _id of the user to delete.

        Returns:
            - 204 status code: If the user was successfully deleted.

        """

        user = _get_user_or_abort_if_doesnt_exist(_id)
        purses = Purse.query.filter_by(user_id=_id).all()
        user.is_active = False
        logging.info("Deleted user %s. Deleting user's purses.", _id)
        for purse in purses:
            purse.is_active = False
            logging.info("Deleted purse %s.", purse.id)
        logging.info("Deleted user %s's purses.", _id)
        db.session.commit()
        return "", 204

    def put(self, _id):
        """
        Updates the user with the given _id.

        Args:
        - _id (int): The _id of the user to update.

        Returns:
            - user_dict (dict): A dictionary containing the details of the updated user.
            - 201 status code: If the user was successfully updated.

        """

        user = _get_user_or_abort_if_doesnt_exist(_id)
        args = put_parser.parse_args()
        _validate_args(args)
        args["birth_date"] = datetime.strptime(args["birth_date"], "%Y-%m-%d")
        logging.info(
            "Updating user %s. Old values: {user.to_dict()}. New values: %s.",
            _id,
            args,
        )
        for key, value in args.items():
            if value is not None:
                setattr(user, key, value)
        db.session.commit()
        return user.to_dict(), 201


class UsersListAPI(Resource):
    """
    Resource for retrieving and creating users.

    Methods:
        - get: Retrieves a list of all users in the database.
        - post: Creates a new user in the database using the details provided in the request.

    Attributes:
        - parser (RequestParser): Parses the arguments of a request.

    """

    def get(self):
        """
        Returns the JSON representation of all users.

        Returns:
            - users_dict (dict): A dictionary containing the details of all users.

        """

        users = User.query.all()
        logging.info("Retrieved all users. Count: %s.", len(users))
        return [user.to_dict() for user in users]

    def post(self):
        """
        Creates a new user.

        Returns:
            - user_dict (dict): A dictionary containing the details of the created user.
            - 201 status code: If the user was successfully created.

        """

        args = post_parser.parse_args()
        _validate_args(args)
        args["birth_date"] = datetime.strptime(args["birth_date"], "%Y-%m-%d")
        user = User(**args)
        db.session.add(user)
        db.session.commit()
        logging.info("Created new user %s. Details: %s.", user.id, user.to_dict())
        return user.to_dict(), 201

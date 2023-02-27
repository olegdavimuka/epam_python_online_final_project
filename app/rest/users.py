import logging
from datetime import datetime

from flask_restful import Resource, abort, reqparse

from app import api, db
from app.models.purses import Purse
from app.models.users import User


def get_user_or_abort_if_doesnt_exist(id):
    """
    Retrieves a user with the given id from the database or aborts the request
    with a 404 error if it doesn't exist.

    Args:
    - id (int): The id of the user to retrieve.

    Returns:
    - user (user): The user object with the given id.

    Raises:
    - 404 error: If the user with the given id doesn't exist in the database.
    """

    user = User.query.get(id)
    if not user:
        logging.error(f"user {id} doesn't exist.")
        abort(404, message=f"user {id} doesn't exist.")
    return user


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
    def get(self, id):
        """
        Returns the JSON representation of a user with the given id.

        Args:
        - id (int): The id of the user to retrieve.

        Returns:
        - user_dict (dict): A dictionary containing the details of the user.
        """

        user = get_user_or_abort_if_doesnt_exist(id)
        logging.info(f"Retrieved user {id}. Details: {user.to_dict()}.")
        return user.to_dict()

    def delete(self, id):
        """
        Deletes the user with the given id from the database.

        Args:
        - id (int): The id of the user to delete.

        Returns:
        - 204 status code: If the user was successfully deleted.
        """

        user = get_user_or_abort_if_doesnt_exist(id)
        purses = Purse.query.filter_by(user_id=id).all()
        db.session.delete(user)
        logging.info(f"Deleted user {id}. Deleting user's purses.")
        for purse in purses:
            db.session.delete(purse)
            logging.info(f"Deleted purse {purse.id}.")
        logging.info(f"Deleted user {id}'s purses.")
        db.session.commit()
        return "", 204

    def put(self, id):
        """
        Updates the user with the given id.

        Args:
        - id (int): The id of the user to update.

        Returns:
        - user_dict (dict): A dictionary containing the details of the updated user.
        - 201 status code: If the user was successfully updated.
        """

        user = get_user_or_abort_if_doesnt_exist(id)
        args = put_parser.parse_args()
        args["birth_date"] = datetime.strptime(args["birth_date"], "%Y-%m-%d")
        logging.info(
            f"Updating user {id}. Old values: {user.to_dict()}. New values: {args}."
        )
        for key, value in args.items():
            if value is not None:
                setattr(user, key, value)
        db.session.commit()
        return user.to_dict(), 201


class UsersListAPI(Resource):
    def get(self):
        """
        Returns the JSON representation of all users.

        Returns:
        - users_dict (dict): A dictionary containing the details of all users.
        """

        users = User.query.all()
        logging.info(f"Retrieved all users. Count: {len(users)}.")
        return [user.to_dict() for user in users]

    def post(self):
        """
        Creates a new user.

        Returns:
        - user_dict (dict): A dictionary containing the details of the created user.
        - 201 status code: If the user was successfully created.
        """

        args = post_parser.parse_args()
        args["birth_date"] = datetime.strptime(args["birth_date"], "%Y-%m-%d")
        user = User(**args)
        db.session.add(user)
        db.session.commit()
        logging.info(f"Created new user {user.id}. Details: {user.to_dict()}.")
        return user.to_dict(), 201


api.add_resource(UsersListAPI, "/api/users")
api.add_resource(UsersAPI, "/api/users/<int:id>")

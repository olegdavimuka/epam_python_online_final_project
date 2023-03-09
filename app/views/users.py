"""
This module defines the UserBlueprint class which is a subclass of the Flask Blueprint class.
It is used to define the routes for the users blueprint. The blueprint provides endpoints for
creating a new user, retrieving a list of all users, retrieving a single user, updating a user,
and deleting a user. The blueprint also provides a search endpoint for searching for users.

Dependencies:
    - logging
    - sqlalchemy
    - flask
    - sqlalchemy.exc
    - app.db
    - app.forms.users
    - app.models.purses
    - app.models.users

Exported classes:
    - UserBlueprint

Functions:
    - make_query: Creates a query for the list endpoint.

"""

import logging

import sqlalchemy as sa
from flask import Blueprint, abort, render_template, request
from sqlalchemy.exc import IntegrityError

from app import db
from app.forms.users import SearchForm, UserForm
from app.models.purses import Purse
from app.models.users import User

PER_PAGE = 10


def make_query():
    """
    Creates a query for the list endpoint. The query is created based on the search parameters
    provided in the request. The query is then paginated and returned.

    Returns:
        - users (query): A query for the list endpoint.

    """

    logging.info("making users query: start")
    users_query = (
        db.session.query(
            User,
            sa.func.count(Purse.id).label(  # pylint: disable=not-callable
                "purse_count"
            ),
        )
        .outerjoin(Purse)
        .filter(
            User.is_active == True  # pylint: disable=singleton-comparison # noqa: E712
        )
        .group_by(User.id)
    )

    if request.args.get("search"):
        search = request.args.get("search").strip()
        checks = [
            User.username.ilike(f"%{search}%"),
            User.email.ilike(f"%{search}%"),
            User.phone.ilike(f"%{search}%"),
            User.first_name.ilike(f"%{search}%"),
            User.last_name.ilike(f"%{search}%"),
        ]
        logging.info("making users query: search")
        users_query = users_query.filter(sa.or_(*checks))

    if (
        request.args.get("birth_date") is not None
        and request.args.get("birth_date") != ""
    ):
        birth_date = request.args.get("birth_date").split(" - ")
        logging.info("making users query: filter by birth_date")
        users_query = users_query.filter(
            sa.and_(User.birth_date >= birth_date[0], User.birth_date <= birth_date[-1])
        )

    if (
        request.args.get("date_created") is not None
        and request.args.get("date_created") != ""
    ):
        date_created = request.args.get("date_created").split(" - ")
        logging.info("making users query: filter by date_created")
        users_query = users_query.filter(
            sa.and_(
                User.date_created >= date_created[0] + " 00:00:00",
                User.date_created <= date_created[-1] + " 23:59:59",
            )
        )

    if (
        request.args.get("date_modified") is not None
        and request.args.get("date_modified") != ""
    ):
        date_modified = request.args.get("date_modified").split(" - ")
        logging.info("making users query: filter by date_modified")
        users_query = users_query.filter(
            sa.and_(
                User.date_modified >= date_modified[0] + " 00:00:00",
                User.date_modified <= date_modified[-1] + " 23:59:59",
            )
        )

    logging.info("making users query: finish")
    return users_query


class UserBlueprint(Blueprint):
    """
    This class is a subclass of the Flask Blueprint class. It is used to define the routes for the
    users blueprint. The blueprint provides endpoints for creating a new user, retrieving a list
    of all users, retrieving a single user, updating a user, and deleting a user. The blueprint
    also provides a search endpoint for searching for users.

    Attributes:
        - name (str): The name of the blueprint.
        - import_name (str): The name of the module or package that the blueprint is defined in.
        - url_prefix (str): The prefix that will be prepended to all of the routes defined in the
        blueprint.

    Methods:
        - list: Retrieves a list of all users.
        - edit: Retrieves a single user or creates a new user.
        - delete: Deletes a single user.
        - _add_constants_to_context: Adds constants to the context dictionary.

    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the UserBlueprint class.

        Args:
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

        """

        super().__init__(*args, **kwargs)
        self.add_url_rule("/", view_func=self.list)
        self.add_url_rule(
            "/<int:_id>", view_func=self.edit, methods=["GET", "POST", "PUT"]
        )
        self.add_url_rule("/<int:_id>", view_func=self.delete, methods=["DELETE"])

    def _add_constants_to_context(self, context):
        """
        Adds constants to the context dictionary.

        Args:
            - context (dict): The context dictionary.

        """

        context.update(
            len=len,
        )

    def list(self):
        """
        Retrieves a list of all users. The list is paginated and returned.

        """

        context = {}
        self._add_constants_to_context(context)

        form = SearchForm()
        form.validate()
        context["form"] = form

        users = make_query()

        context["page"] = request.args.get("page", 1, type=int)
        context["pagination"] = users.paginate(
            page=context["page"], per_page=PER_PAGE, error_out=False
        )
        context["url"] = "user_bp.list"

        logging.info("Retrieved all users. Count: %s.", len(users.all()))
        return render_template("users/list.html", **context)

    def edit(self, _id):
        """
        Retrieves a single user, edits the user, or creates a new user.

        Args:
            - _id (int): The id of the user to retrieve.

        """

        _id = int(_id)

        context = {}

        if _id == 0:
            context["user"] = {}
            user = User()
        else:
            user = User.query.get(_id)

        if not user:
            logging.error("User %s does not exist.", _id)
            abort(404, message=f"User with id {_id} does not exist.")

        form = UserForm()
        if request.method == "POST":
            formdata = request.form
            form = UserForm(formdata=formdata, _id=_id)

            if not form.validate():
                context["errors"] = form.errors
            else:
                user.update(**dict(form.data.items()))

                if _id == 0:
                    db.session.add(user)
                    logging.info("Created new user with id %s.", user.id)
                else:
                    logging.info("Updated user %s.", _id)

                db.session.commit()
                context["success"] = True

        context["form"] = form
        context["user"] = user

        logging.info("Retrieved user %s.", _id)
        return render_template("users/edit.html", **context)

    def delete(self, _id):  # pylint: disable=arguments-differ
        """
        Deletes a single user.

        Args:
            - _id (int): The id of the user to delete.

        Returns:
            - message (str): A message indicating whether the user was deleted or not.
            - status (int): The status code.

        """

        _id = int(_id)
        user = User.query.get(_id)
        purses = Purse.query.filter_by(user_id=_id).all()

        try:
            for purse in purses:
                purse.is_active = False
            user.is_active = False
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"message": "User cannot be deleted"}, 400

        logging.info("Deleted user %s.", _id)
        logging.info("Deleted %s purses for user %s.", len(purses), _id)
        return {"message": "User deleted"}, 200

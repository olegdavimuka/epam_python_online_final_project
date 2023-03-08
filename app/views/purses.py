"""
This module defines the PurseBlueprint class which is a subclass of the Flask Blueprint class.
It is used to define the routes for the purses blueprint. The blueprint provides endpoints for
creating a new purse, retrieving a list of all purses, retrieving a single purse, and deleting
a purse. The blueprint also provides a search endpoint for searching for purses.

Dependencies:
    - logging
    - sqlalchemy
    - flask
    - sqlalchemy.exc
    - app.db
    - app.constants.rates
    - app.forms.purses
    - app.models.purses
    - app.models.users

Exported classes:
    - PurseBlueprint

Functions:
    - make_query: Creates a query for the list endpoint.

"""

import logging

import sqlalchemy as sa
from flask import Blueprint, abort, render_template, request
from sqlalchemy.exc import IntegrityError

from app import db
from app.constants.rates import Currency, Rates
from app.forms.purses import PurseForm, SearchForm
from app.models.purses import Purse
from app.models.users import User

PER_PAGE = 10


def make_query():
    """
    Creates a query for the list endpoint. The query is created based on the search parameters
    provided in the request. The query is then paginated and returned.

    Returns:
        - purses (query): A query for the list endpoint.

    """

    purses_query = db.session.query(
        Purse,
    ).filter(
        Purse.is_active == True  # pylint: disable=singleton-comparison # noqa: E712
    )

    if request.args.get("search"):
        search = request.args.get("search").strip()
        checks = [
            Purse.currency.ilike(f"%{search}%"),
        ]
        try:
            int_search = int(search)
        except ValueError:
            pass
        else:
            checks.extend(
                [
                    Purse.user_id == int_search,
                ]
            )
        logging.info("making purses query: search")
        purses_query = purses_query.filter(sa.or_(*checks))

    if request.args.get("user_id"):
        user_id = request.args.get("user_id")
        logging.info("making purses query: filter by user id")
        purses_query = purses_query.filter(Purse.user_id == user_id)

    if request.args.get("currency"):
        currency = request.args.get("currency")
        logging.info("making purses query: filter by currency")
        purses_query = purses_query.filter(Purse.currency == currency)

    if (
        request.args.get("date_created") is not None
        and request.args.get("date_created") != ""
    ):
        date_created = request.args.get("date_created").split(" - ")
        logging.info("making purses query: filter by date created")
        purses_query = purses_query.filter(
            sa.and_(
                Purse.date_created >= date_created[0] + " 00:00:00",
                Purse.date_created <= date_created[-1] + " 23:59:59",
            )
        )

    if (
        request.args.get("date_modified") is not None
        and request.args.get("date_modified") != ""
    ):
        date_modified = request.args.get("date_modified").split(" - ")
        logging.info("making purses query: filter by date modified")
        purses_query = purses_query.filter(
            sa.and_(
                Purse.date_modified >= date_modified[0] + " 00:00:00",
                Purse.date_modified <= date_modified[-1] + " 23:59:59",
            )
        )

    logging.info("making purses query: finish")
    return purses_query


class PurseBlueprint(Blueprint):
    """
    This class is a subclass of the Flask Blueprint class. It is used to define the routes for the
    purses blueprint. The blueprint provides endpoints for creating a new purse, retrieving a list
    of all purses, retrieving a single purse, and deleting a purse. The blueprint also provides a
    search endpoint for searching for purses.

    Attributes:
        - name (str): The name of the blueprint.
        - import_name (str): The name of the module or package that the blueprint is defined in.
        - url_prefix (str): The prefix that will be prepended to all of the routes defined in the
        blueprint.

    Methods:
        - list: Retrieves a list of all purses.
        - edit: Retrieves a single purse or creates a new purse.
        - delete: Deletes a single purse.
        - _add_constants_to_context: Adds constants to the context dictionary.

    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the PurseBlueprint class.

        Args:
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

        """

        super().__init__(*args, **kwargs)
        self.add_url_rule("/", view_func=self.list)
        self.add_url_rule("/<int:_id>", view_func=self.edit, methods=["GET", "POST"])
        self.add_url_rule("/<int:_id>", view_func=self.delete, methods=["DELETE"])

    def _add_constants_to_context(self, context):
        """
        Adds constants to the context dictionary.

        Args:
            - context (dict): The context dictionary.

        """

        context.update(
            Currency=Currency,
            Rates=Rates,
        )

    def list(self):
        """
        Retrieves a list of all purses. The list is paginated and returned.

        """

        context = {}
        self._add_constants_to_context(context)

        form = SearchForm()
        form.validate()
        context["form"] = form
        context["users"] = User.query.all()

        purses = make_query()

        context["page"] = request.args.get("page", 1, type=int)
        context["pagination"] = purses.paginate(
            page=context["page"], per_page=PER_PAGE, error_out=False
        )
        context["url"] = "purse_bp.list"

        logging.info("Retrieved all purses. Count: %s.", len(purses.all()))
        return render_template("purses/list.html", **context)

    def edit(self, _id):
        """
        Retrieves a single purse, edits the purse, or creates a new purse.

        Args:
            - _id (int): The id of the purse to retrieve.

        """

        _id = int(_id)

        context = {}
        self._add_constants_to_context(context)

        if _id == 0:
            context["purse"] = {}
            purse = Purse()
        else:
            purse = Purse.query.get(_id)

        if not purse:
            logging.error("Purse %s does not exist.", _id)
            abort(404, message=f"Purse with id {_id} does not exist.")

        form = PurseForm()
        if request.method == "POST":
            formdata = request.form
            form = PurseForm(formdata=formdata, _id=_id)

            if not form.validate():
                context["errors"] = form.errors
            else:
                purse.update(**dict(form.data.items()))

                db.session.add(purse)
                logging.info("Created new purse with id %s.", purse.id)

                db.session.commit()
                context["success"] = True

        context["form"] = form
        context["purse"] = purse
        context["users"] = User.query.all()

        logging.info("Retrieved purse %s.", _id)
        return render_template("purses/edit.html", **context)

    def delete(self, _id):  # pylint: disable=arguments-differ
        """
        Deletes a single purse.

        Args:
            - _id (int): The id of the purse to delete.

        Returns:
            - message (str): A message indicating whether the purse was deleted or not.
            - status (int): The status code.

        """

        _id = int(_id)
        purse = Purse.query.get(_id)

        try:
            purse.is_active = False
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"message": "Purse cannot be deleted"}, 400

        logging.info("Deleted purse %s.", _id)
        return {"message": "Purse deleted"}, 200

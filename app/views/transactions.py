"""
This module defines the TransactionBlueprint class which is a subclass of the Flask Blueprint class.
It is used to define the routes for the transactions blueprint. The blueprint provides endpoints for
creating a new transaction, retrieving a list of all transaction and retrieving a single
transaction. The blueprint also provides a search endpoint for searching for transactions.

Dependencies:
    - logging
    - sqlalchemy
    - flask
    - app.db
    - app.constants.rates
    - app.forms.transactions
    - app.models.purses
    - app.models.transactions

Exported classes:
    - TransactionBlueprint

Functions:
    - make_query: Creates a query for the list endpoint.

"""

import logging

import sqlalchemy as sa
from flask import Blueprint, abort, render_template, request

from app import db
from app.constants.rates import Currency, Rates
from app.forms.transactions import SearchForm, TransactionForm
from app.models.purses import Purse
from app.models.transactions import Transaction

PER_PAGE = 10


def make_query():
    """
    Creates a query for the list endpoint. The query is created based on the search parameters
    provided in the request. The query is then paginated and returned.

    Returns:
        - purses (query): A query for the list endpoint.

    """

    logging.info("making transaction query: start")
    transactions_query = db.session.query(
        Transaction,
    )

    if request.args.get("search"):
        search = request.args.get("search").strip()
        checks = [
            Transaction.purse_from_currency.ilike(f"%{search}%"),
            Transaction.purse_to_currency.ilike(f"%{search}%"),
        ]
        try:
            int_search = int(search)
        except ValueError:
            pass
        else:
            checks.extend(
                [
                    Transaction.purse_from_id == int_search,
                    Transaction.purse_to_id == int_search,
                ]
            )
        logging.info("making transactions query: search")
        transactions_query = transactions_query.filter(sa.or_(*checks))

    if request.args.get("purse_from_id"):
        purse_from_id = request.args.get("purse_from_id")
        logging.info("making transactions query: filter by purse_from_id")
        transactions_query = transactions_query.filter(
            Transaction.purse_from_id == purse_from_id
        )

    if request.args.get("purse_to_id"):
        purse_to_id = request.args.get("purse_to_id")
        logging.info("making transactions query: filter by purse_to_id")
        transactions_query = transactions_query.filter(
            Transaction.purse_to_id == purse_to_id
        )

    if request.args.get("purse_from_currency"):
        purse_from_currency = request.args.get("purse_from_currency")
        logging.info("making transactions query: filter by purse_from_currency")
        transactions_query = transactions_query.filter(
            Transaction.purse_from_currency == purse_from_currency
        )

    if request.args.get("purse_to_currency"):
        purse_to_currency = request.args.get("purse_to_currency")
        logging.info("making transactions query: filter by purse_to_currency")
        transactions_query = transactions_query.filter(
            Transaction.purse_to_currency == purse_to_currency
        )

    if (
        request.args.get("date_created") is not None
        and request.args.get("date_created") != ""
    ):
        date_created = request.args.get("date_created").split(" - ")
        logging.info("making transactions query: filter by date created")
        transactions_query = transactions_query.filter(
            sa.and_(
                Purse.date_created >= date_created[0] + " 00:00:00",
                Purse.date_created <= date_created[-1] + " 23:59:59",
            )
        )

    logging.info("making transactions query: finish")
    return transactions_query


class TransactionBlueprint(Blueprint):
    """
    This class is a subclass of the Flask Blueprint class. It is used to define the routes for the
    transactions blueprint. The blueprint provides endpoints for creating a new transaction,
    retrieving a list of all transactions, and retrieving a single transaction, The blueprint
    also provides a search endpoint for searching for transactions.

    Attributes:
        - name (str): The name of the blueprint.
        - import_name (str): The name of the module or package that the blueprint is defined in.
        - url_prefix (str): The prefix that will be prepended to all of the routes defined in the
        blueprint.

    Methods:
        - list: Retrieves a list of all purses.
        - edit: Retrieves a single purse or creates a new purse.
        - _add_constants_to_context: Adds constants to the context dictionary.

    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the TransactionBlueprint class.

        Args:
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

        """

        super().__init__(*args, **kwargs)
        self.add_url_rule("/", view_func=self.list)
        self.add_url_rule("/<int:_id>", view_func=self.edit, methods=["GET", "POST"])

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
        Retrieves a list of all transactions. The list is paginated and returned.

        """

        context = {}
        self._add_constants_to_context(context)

        form = SearchForm()
        form.validate()
        context["form"] = form
        context["purses"] = Purse.query.all()

        transactions = make_query()

        context["page"] = request.args.get("page", 1, type=int)
        context["pagination"] = transactions.paginate(
            page=context["page"], per_page=PER_PAGE, error_out=False
        )
        context["url"] = "transaction_bp.list"

        logging.info("Retrieved all transactions. Count: %s.", len(transactions.all()))
        return render_template("transactions/list.html", **context)

    def edit(self, _id):
        """
        Retrieves a single transaction or creates a new transaction.

        Args:
            - _id (int): The id of the transaction to retrieve.

        """

        _id = int(_id)

        context = {}
        self._add_constants_to_context(context)

        if _id == 0:
            context["transaction"] = {}
            transaction = Transaction()
        else:
            transaction = Transaction.query.get(_id)

        if not transaction:
            logging.error("Transaction %s does not exist.", _id)
            abort(404, f"Transaction with id {_id} does not exist.")

        form = TransactionForm()
        if request.method == "POST":
            formdata = request.form
            form = TransactionForm(formdata=formdata, _id=_id)

            if not form.validate():
                context["errors"] = form.errors
            else:
                transaction.update(**dict(form.data.items()))

                db.session.add(transaction)
                logging.info("Created new transaction with id %s.", transaction.id)

                db.session.commit()
                context["success"] = True

        context["form"] = form
        context["transaction"] = transaction
        context["purses"] = Purse.query.all()

        logging.info("Retrieved transaction %s.", _id)
        return render_template("transactions/edit.html", **context)

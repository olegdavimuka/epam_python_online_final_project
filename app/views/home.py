"""
This module contains the HomeView class, which is used to render the home page. The home page
displays a list of all currencies and their exchange rates. The HomeView class is a subclass of
the Flask View class. It is used to render the home page.

Dependencies:
    - flask
    - flask.views
    - app
    - app.constants.rates
    - app.service.populate_db

Exported classes:
    - HomeView

"""

from flask import render_template
from flask.views import View

from app import db
from app.constants.rates import Currency, Rates
from app.service.populate_db import populate_db


class HomeView(View):
    """
    View for the home page.

    Attributes:
        - context (dict): a dictionary containing data to be passed to the template
        when rendering the page.

    Methods:
        - __init__() - initializes an instance of HomeView class.
        - _add_constants_to_context(context) - adds constants to the context dictionary.
        - dispatch_request() - renders the home template with the given context.

    """

    def __init__(self):
        """
        Initializes an instance of HomeView class.

        Parameters:
            - context (dict): a dictionary containing data to be passed to the template
            when rendering the page.

        """

        self.context = {}

    def _add_constants_to_context(self, context):
        """
        Adds constants to the context dictionary.

        Parameters:
            - context (dict): a dictionary to which the constants will be added.

        """

        context.update(
            Currency=Currency,
            Rates=Rates,
        )

    def dispatch_request(self):
        """
        Renders the home template with the given context.

        Returns:
            - str: the rendered HTML template.

        """

        context = self.context
        self._add_constants_to_context(context)

        # drop and recreate the database, and populate it with data
        db.drop_all()
        db.create_all()
        populate_db(db)

        return render_template("home.html", **context)

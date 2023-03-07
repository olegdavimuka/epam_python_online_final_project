"""
This module provides base search functionality in a Flask web application. The module provides a
base form for search functionality with three optional fields: `search`, `date_created`, and
`date_modified`.

Dependencies:
    - flask_wtf
    - wtforms
    - wtforms.validators

Exported classes:
    - BaseSearchForm

"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Optional


class BaseSearchForm(FlaskForm):
    """
    A base form for search with optional fields. This class provides a base form for search
    functionality with three optional fields: `search`, `date_created`, and `date_modified`.

    Attributes:
        - search (StringField): The search field for filtering search results.
        - date_created (StringField): The date created field for filtering search results
        by creation date.
        - date_modified (StringField): The date modified field for filtering search results
        by modification date.

    """

    search = StringField("Search", validators=[Optional()])
    date_created = StringField(validators=[Optional()])
    date_modified = StringField(validators=[Optional()])

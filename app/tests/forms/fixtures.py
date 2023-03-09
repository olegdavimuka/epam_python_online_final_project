"""
This module contains the fixtures for the tests for the forms module.

Dependencies:
    - pytest
    - flask

Functions:
    - app(): returns a Flask app object.

"""

import pytest
from flask import Flask


@pytest.fixture(name="app")
def fixture_app():
    """
    This fixture returns a Flask app object.

    Returns:
        - app: A Flask app object.

    """

    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    return app

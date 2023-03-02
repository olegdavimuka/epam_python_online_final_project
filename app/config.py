"""
This module contains the configuration dataclasses for the Flask application.

Dependencies:
    - os
    - dataclasses

Exported Classes:
    - Config: The base configuration class.
    - TestingConfig(Config): The configuration class for running tests.

"""

import dataclasses
import os


@dataclasses.dataclass
class Config:
    """
    The base configuration class for the Flask application.

    Attributes:
        - SECRET_KEY (str): The secret key for the Flask app.
        - SQLALCHEMY_DATABASE_URI (str): The URI of the database to use.
        - SQLALCHEMY_TRACK_MODIFICATIONS (bool): Whether to track modifications to the database.
        - DEBUG (bool): Whether to run the app in debug mode.

    """

    SECRET_KEY = os.environ.get("SECRET_KEY") or "my-secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + "dev.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


@dataclasses.dataclass
class TestingConfig(Config):
    """
    The configuration class for running tests.

    Attributes:
        - SQLALCHEMY_DATABASE_URI (str): The URI of the test database to use.
        - TESTING (bool): Whether the app is running in test mode.
        - DEBUG (bool): Whether to run the app in debug mode during tests.

    """

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL") or "sqlite:///" + "test.db"
    )
    TESTING = True
    DEBUG = False

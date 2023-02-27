import os

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from app.utils.logging import setup_logging

app = Flask(__name__)
api = Api(app)

SECRET_KEY = os.urandom(32)

app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///e-wallet.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

setup_logging()

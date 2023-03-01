from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from app.config import Config
from app.utils.logging import setup_logging

db = SQLAlchemy()
migrate = Migrate(db)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.rest.purses import PursesAPI, PursesListAPI
    from app.rest.transactions import TransactionsAPI, TransactionsListAPI
    from app.rest.users import UsersAPI, UsersListAPI

    api = Api(prefix="/api")
    api.add_resource(UsersListAPI, "/users")
    api.add_resource(UsersAPI, "/users/<int:id>")
    api.add_resource(PursesListAPI, "/purses")
    api.add_resource(PursesAPI, "/purses/<int:id>")
    api.add_resource(TransactionsListAPI, "/transactions")
    api.add_resource(TransactionsAPI, "/transactions/<int:id>")

    api.init_app(app)

    setup_logging()

    return app

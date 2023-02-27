import unittest
from unittest.mock import patch

from flask import Flask
from flask_restful import Api

from app import db
from app.models.purses import Purse
from app.rest.purses import get_purse_or_abort_if_doesnt_exist, parser


class TestPursesAPI(unittest.TestCase):
    """
    Test class for testing the Purse API.
    """

    def setUp(self):
        """
        Set up the Flask app and create a test client.
        Also, initialize the database and create all the tables.
        """

        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.app = app.test_client()
        db.init_app(app)
        with app.app_context():
            db.create_all()
        self.api = Api(app)

    def tearDown(self):
        """
        Remove the database session and drop all tables after each test.
        """

        with self.app.application.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_purse_or_abort_if_doesnt_exist(self):
        """
        Test function to check if the purse exists in the database or not.
        """

        with self.assertRaises(Exception) as context:
            get_purse_or_abort_if_doesnt_exist(1)
        self.assertEqual(context.exception.code, 404)

        purse = Purse(user_id=1, currency="USD")
        db.session.add(purse)
        db.session.commit()

        self.assertEqual(get_purse_or_abort_if_doesnt_exist(purse.id), purse)

    def test_PursesAPI_get(self):
        """
        Test function to get a specific purse from the API.
        """

        purse = Purse(user_id=1, currency="USD")
        db.session.add(purse)
        db.session.commit()

        response = self.app.get(f"/api/purses/{purse.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, purse.to_dict())

    def test_PursesAPI_delete(self):
        """
        Test function to delete a specific purse from the API.
        """

        purse = Purse(user_id=1, currency="USD")
        db.session.add(purse)
        db.session.commit()

        response = self.app.delete(f"/api/purses/{purse.id}")
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(Purse.query.get(purse.id))

    def test_PursesListAPI_get(self):
        """
        Test function to get a list of all the purses from the API.
        """

        purses = [Purse(user_id=1, currency="USD") for i in range(3)]
        db.session.add_all(purses)
        db.session.commit()

        response = self.app.get("/api/purses")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [purse.to_dict() for purse in purses])

    @patch.object(parser, "parse_args", return_value={"user_id": 1, "currency": "USD"})
    def test_PursesListAPI_post(self, mock_parse_args):
        """
        Test function to add a new purse to the API.
        """

        response = self.app.post("/api/purses")
        self.assertEqual(response.status_code, 201)

        purse = Purse.query.filter_by(id=response.json["id"]).first()
        self.assertIsNotNone(purse)
        self.assertEqual(purse.user_id, 1)
        self.assertEqual(purse.currency, "USD")


if __name__ == "__main__":
    unittest.main()

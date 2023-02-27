import unittest

from flask import Flask

from app import api, app, db
from app.models.transactions import Transaction
from app.rest.transactions import TransactionsAPI, TransactionsListAPI


class TestTransactionsAPI(unittest.TestCase):
    """
    Test class for testing the Transaction API.
    """

    def setUp(self):
        """
        Setup method that creates an in-memory SQLite database and initializes
        the test client and database with a single transaction.
        """

        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)
        with app.app_context():
            db.create_all()
        api.add_resource(TransactionsListAPI, "/api/transactions")
        api.add_resource(TransactionsAPI, "/api/transactions/<int:id>")
        self.client = app.test_client()
        self.transaction = Transaction(
            purse_from_id=1, purse_to_id=2, purse_from_amount=10
        )
        with app.app_context():
            db.session.add(self.transaction)
            db.session.commit()

    def tearDown(self):
        """
        Tear-down method that drops all tables from the in-memory database.
        """

        with app.app_context():
            db.drop_all()

    def test_get_transaction(self):
        """
        Tests that a GET request to retrieve a transaction
        by its ID returns the correct transaction and status code.
        """

        response = self.client.get(f"/api/transactions/{self.transaction.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, self.transaction.to_dict())

    def test_get_transaction_doesnt_exist(self):
        """
        Tests that a GET request to retrieve a non-existent
        transaction returns a 404 status code.
        """

        response = self.client.get(f"/api/transactions/{self.transaction.id + 1}")
        self.assertEqual(response.status_code, 404)

    def test_get_transactions_list(self):
        """
        Tests that a GET request to retrieve a list of
        all transactions returns the correct list and status code.
        """

        response = self.client.get("/api/transactions")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0], self.transaction.to_dict())

    def test_post_transaction(self):
        """
        Tests that a POST request to create a new transaction
        with valid data returns a 201 status code and that
        the transaction is added to the database.
        """

        new_transaction_data = {
            "purse_from_id": 2,
            "purse_to_id": 1,
            "purse_from_amount": 5,
        }
        response = self.client.post("/api/transactions", data=new_transaction_data)
        self.assertEqual(response.status_code, 201)
        new_transaction = Transaction.query.filter_by(id=response.json["id"]).first()
        self.assertIsNotNone(new_transaction)
        self.assertEqual(new_transaction.purse_from_id, 2)
        self.assertEqual(new_transaction.purse_to_id, 1)
        self.assertEqual(new_transaction.purse_from_amount, 5)

    def test_post_transaction_missing_required_field(self):
        """
        Tests that a POST request to create a new transaction
        with missing required fields returns a 400 status code.
        """

        new_transaction_data = {"purse_to_id": 1, "purse_from_amount": 5}
        response = self.client.post("/api/transactions", data=new_transaction_data)
        self.assertEqual(response.status_code, 400)

    def test_post_transaction_invalid_field_type(self):
        """
        Tests that a POST request to create a new transaction
        with invalid field types returns a 400 status code.
        """

        new_transaction_data = {
            "purse_from_id": "not_an_int",
            "purse_to_id": 1,
            "purse_from_amount": 5,
        }
        response = self.client.post("/api/transactions", data=new_transaction_data)
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()

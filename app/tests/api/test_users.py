import unittest
from datetime import datetime

from app import app, db
from app.models.users import User


class TestUserAPI(unittest.TestCase):
    """
    Test class for testing the User API.
    """

    def setUp(self):
        """
        Set up the test database and create a test client.
        """

        self.client = app.test_client()
        self.user = User(
            username="testuser",
            email="testuser@test.com",
            phone="+12345678901",
            first_name="Test",
            last_name="User",
            birth_date=datetime.strptime("2000-01-01", "%Y-%m-%d"),
        )
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """
        Drop the test database.
        """

        db.session.delete(self.user)
        db.session.commit()

    def test_get_user(self):
        """
        Test retrieving a user with a given ID.
        """

        response = self.client.get(f"/api/users/{self.user.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, self.user.to_dict())

    def test_get_nonexistent_user(self):
        """
        Test retrieving a nonexistent user.
        """

        response = self.client.get("/api/users/999")
        self.assertEqual(response.status_code, 404)

    def test_delete_user(self):
        """
        Test deleting a user with a given ID.
        """

        response = self.client.delete(f"/api/users/{self.user.id}")
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(User.query.get(self.user.id))

    def test_put_user(self):
        """
        Test updating a user with a given ID.
        """

        updated_user_data = {
            "username": "updateduser",
            "email": "updateduser@test.com",
            "phone": "+12345678901",
            "first_name": "Updated",
            "last_name": "User",
            "birth_date": "2000-01-01",
        }
        response = self.client.put(f"/api/users/{self.user.id}", data=updated_user_data)
        self.assertEqual(response.status_code, 201)
        updated_user = User.query.get(self.user.id)
        self.assertEqual(updated_user.username, updated_user_data["username"])
        self.assertEqual(updated_user.email, updated_user_data["email"])
        self.assertEqual(updated_user.phone, updated_user_data["phone"])
        self.assertEqual(updated_user.first_name, updated_user_data["first_name"])
        self.assertEqual(updated_user.last_name, updated_user_data["last_name"])
        self.assertEqual(
            updated_user.birth_date,
            datetime.strptime(updated_user_data["birth_date"], "%Y-%m-%d"),
        )

    def test_put_nonexistent_user(self):
        """
        Test updating a nonexistent user.
        """

        updated_user_data = {
            "username": "updateduser",
            "email": "updateduser@test.com",
            "phone": "+12345678901",
            "first_name": "Updated",
            "last_name": "User",
            "birth_date": "2000-01-01",
        }
        response = self.client.put("/api/users/999", data=updated_user_data)
        self.assertEqual(response.status_code, 404)

    def test_create_user(self):
        """
        Test creating a new user.
        """

        new_user_data = {
            "username": "newuser",
            "email": "newuser@test.com",
            "phone": "+12345678901",
            "first_name": "New",
            "last_name": "User",
            "birth_date": "2000-01-01",
        }
        response = self.client.post("/api/users", data=new_user_data)
        self.assertEqual(response.status_code, 201)
        new_user = User.query.filter_by(username=new_user_data["username"]).first()
        self.assertEqual(new_user.username, new_user_data["username"])
        self.assertEqual(new_user.email, new_user_data["email"])
        self.assertEqual(new_user.phone, new_user_data["phone"])
        self.assertEqual(new_user.first_name, new_user_data["first_name"])
        self.assertEqual(new_user.last_name, new_user_data["last_name"])
        self.assertEqual(
            new_user.birth_date,
            datetime.strptime(new_user_data["birth_date"], "%Y-%m-%d"),
        )

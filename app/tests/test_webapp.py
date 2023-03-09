"""
This module contains the tests for the Flask app.

Dependencies:
    - app

Classes:
    - TestApp: A class that contains the tests for the Flask app.

"""

import app


class TestWebapp:
    """
    This class contains the tests for the Flask app.

    Methods:
        - test_app_creation(): tests the creation of the Flask app.
        - test_app_run(): tests the running of the Flask app.

    """

    def test_app_creation(self):
        """
        Test that create_app() returns a non-None object.

        """

        assert app.create_app() is not None

    def test_app_run(self):
        """
        Test that the Flask app runs and returns a 200 status code.

        """

        test_app = app.create_app()
        with test_app.test_client() as client:
            response = client.get("/")
            assert response.status_code == 200

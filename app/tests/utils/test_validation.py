"""
This module contains the tests for the validation module.

Dependencies:
    - re
    - faker
    - app.tests.api.fixtures
    - app.utils.validation

Classes:
    - TestValidation: A class that contains the tests for the validation module.

"""

import re

from faker import Faker

from app.tests.api.fixtures import (  # noqa: F401 pylint: disable=unused-import
    fixture_app,
    fixture_user,
)
from app.utils.validation import (
    fake_phone_number,
    is_free_email,
    is_free_phone_number,
    is_free_username,
    is_valid_date,
    is_valid_email,
    is_valid_phone_number,
)

fake = Faker()


class TestValidation:
    """
    This class contains the tests for the validation module.

    Methods:
        - test_is_valid_email(): tests the is_valid_email function.
        - test_is_valid_phone_number(): tests the is_valid_phone_number function.
        - test_is_free_username(user): tests the is_free_username function.
        - test_is_free_email(user): tests the is_free_email function.
        - test_is_free_phone_number(user): tests the is_free_phone_number function.
        - test_is_valid_date(): tests the is_valid_date function.
        - test_fake_phone_number(): tests the fake_phone_number function.

    """

    def test_is_valid_email(self):
        """
        Test is_valid_email function.

        """

        assert is_valid_email(fake.email())
        assert not is_valid_email("userexample.com")
        assert not is_valid_email("user@examplecom")
        assert not is_valid_email("user@.com")

    def test_is_valid_phone_number(self):
        """
        Test is_valid_phone_number function.

        """

        assert is_valid_phone_number(fake_phone_number())
        assert is_valid_phone_number(fake_phone_number())
        assert not is_valid_phone_number("1234567890")
        assert not is_valid_phone_number("+12345678901")
        assert not is_valid_phone_number("+1234567890123")

    def test_is_free_username(self, user):
        """
        Test is_free_username function.

        """

        assert not is_free_username(user.username, 0)
        assert is_free_username(user.username, user.id)

    def test_is_free_email(self, user):
        """
        Test is_free_email function.

        """

        assert not is_free_email(user.email, 0)
        assert is_free_email(user.email, user.id)

    def test_is_free_phone_number(self, user):
        """
        Test is_free_phone_number function.

        """

        assert not is_free_phone_number(user.phone, 0)
        assert is_free_phone_number(user.phone, user.id)

    def test_is_valid_date(self):
        """
        Test is_valid_date function.

        """

        assert is_valid_date(fake.date())
        assert not is_valid_date("2022/12/31")
        assert not is_valid_date("12-31-2022")
        assert not is_valid_date("2022-13-31")
        assert not is_valid_date("2022-12-32")

    def test_fake_phone_number(self):
        """
        Test fake_phone_number function.

        """

        pattern = r"\+\d{11}"
        phone_number = fake_phone_number()
        assert re.match(pattern, phone_number)
        assert phone_number.startswith("+1") or phone_number.startswith("+3")
        assert len(phone_number) == 13

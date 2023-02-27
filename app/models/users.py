import logging
from datetime import datetime

from app import db
from app.utils.validation import is_valid_email, is_valid_phone_number


class User(db.Model):
    """
    A class representing a User entity in the database.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        id (int): The primary key of the User entity.
        username (str): The username of the User.
        email (str): The email address of the User.
        phone (str): The phone number of the User.
        first_name (str): The first name of the User.
        last_name (str): The last name of the User.
        birth_date (datetime.date): The birth date of the User.
        date_created (datetime.datetime): The date and time when the User was created.
        date_modified (datetime.datetime): The date and time when the User was last modified.
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(50), nullable=False, unique=True)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_modified = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, **kwargs):
        """
        Initializes a new user instance.

        Args:
        **kwargs: A dictionary of user attributes.

        Raises:
        ValueError: If the email attribute is not valid,
        or the phone attribute is not valid.
        """

        super(User, self).__init__(**kwargs)

        if not is_valid_email(self.email):
            logging.error("Creating user failed: Email is not valid.")
            raise ValueError("Email is not valid.")

        if not is_valid_phone_number(self.phone):
            logging.error("Creating user failed: Phone number is not valid.")
            raise ValueError("Phone number is not valid.")

    def birth_date_str(self):
        """
        Converts the birth date of the User to a string format.

        Returns:
            str: The birth date of the User in the format '%Y-%m-%d'.
        """

        return self.birth_date.strftime("%Y-%m-%d")

    def date_created_str(self):
        """
        Converts the creation date of the User to a string format.

        Returns:
            str: The creation date of the User in the format '%Y-%m-%d %H:%M:%S'.
        """

        return self.date_created.strftime("%Y-%m-%d %H:%M:%S")

    def date_modified_str(self):
        """
        Converts the modification date of the User to a string format.

        Returns:
            str: The modification date of the User in the format '%Y-%m-%d %H:%M:%S'.
        """

        return self.date_modified.strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        """
        Returns a string representation of the User object.

        Returns:
            str: A string representation of the User object.
        """

        return f"User id: {self.id}, \
            name: {self.name}, \
            email: {self.email}, \
            phone: {self.phone}"

    def to_dict(self):
        """
        Returns a dictionary representation of the User object.

        Returns:
            dict: A dictionary representation of the User object.
        """

        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date_str(),
            "date_created": self.date_created_str(),
            "date_modified": self.date_modified_str(),
        }

from datetime import datetime

from app import db


class User(db.Model):
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

    def date_created_str(self):
        return self.date_created.strftime("%Y-%m-%d %H:%M:%S")

    def date_modified_str(self):
        return self.date_modified.strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return f"User id: {self.id}, \
            name: {self.name}, \
            email: {self.email}, \
            phone: {self.phone}"

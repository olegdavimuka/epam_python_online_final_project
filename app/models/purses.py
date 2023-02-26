from datetime import datetime

from app import db
from app.constants.currency import Currency


class Purse(db.Model):
    __tablename__ = "purses"
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    currency = db.Column(db.Enum(Currency), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_modified = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def date_created_str(self):
        return self.date_created.strftime("%Y-%m-%d %H:%M:%S")

    def date_modified_str(self):
        return self.date_modified.strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return f"Purse id: {self.id}, \
            user_id: {self.user_id}, \
            currency: {self.currency}, \
            balance: {self.balance}"

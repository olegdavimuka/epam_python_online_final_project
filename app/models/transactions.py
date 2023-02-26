from datetime import datetime

from app import db
from app.constants.currency import Currency


class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)

    purse_from_id = db.Column(db.Integer, db.ForeignKey("purses.id"), nullable=False)
    purse_to_id = db.Column(db.Integer, db.ForeignKey("purses.id"), nullable=False)

    purse_from_currency = db.Column(db.Enum(Currency), nullable=False)
    purse_to_currency = db.Column(db.Enum(Currency), nullable=False)

    purse_from_amount = db.Column(db.Float, nullable=False, default=0.0)
    purse_to_amount = db.Column(db.Float, nullable=False, default=0.0)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def date_created_str(self):
        return self.date_created.strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return f"Transaction id: {self.id}, \
            purse_from_id: {self.purse_from_id}, \
            purse_to_id: {self.purse_to_id}, \
            purse_from_currency: {self.purse_from_currency}, \
            purse_to_currency: {self.purse_to_currency}, \
            purse_from_amount: {self.purse_from_amount}, \
            purse_to_amount: {self.purse_to_amount}"

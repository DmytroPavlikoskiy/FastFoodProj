from datetime import datetime
from db_config.db_manager import db


class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    status = db.Column(db.String(20)) # success, failed, pending
    transaction_id = db.Column(db.String(100))
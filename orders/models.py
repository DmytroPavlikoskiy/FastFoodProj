from db_config.db_manager import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(
        db.String(20),
        nullable=False,
        default="pending"
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    delivery_address = db.Column(db.String(255), nullable=False)
    items = db.relationship("OrderItem", backref="order", lazy=True)

    def __repr__(self):
        return f"<Order {self.id} | status={self.status}>"

class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False
    )
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_time = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<OrderItem order={self.order_id} product={self.product_id}>"

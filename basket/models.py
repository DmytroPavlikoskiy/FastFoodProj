from db_config.db_manager import db, get_db
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from users.models import User
from menu.models import Dish



class Basket(db.Model):
    __tablename__ = "baskets"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    user = db.relationship("User", back_populates="basket")
    items = db.relationship("BasketItem", backref="basket", cascade="all, delete-orphan")

class BasketItem(db.Model):
    __tablename__ = "basket_items"
    id = db.Column(db.Integer, primary_key=True)
    basket_id = db.Column(db.Integer, db.ForeignKey("baskets.id"), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey("dishes.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    dish = db.relationship("Dish")
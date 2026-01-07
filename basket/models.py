from db_config.db_manager import db
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from users.models import User
from menu.models import Products



class BasketItem(db.Model):
    tablename = "basket_items"

    id = Column(Integer, primary_key=True)
    product_id = ForeignKey(Integer, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

     
    product_relalationship = relationship("Products", backref="basket_item")
    def repr(self):
        return (
            f"<BasketItem user_id={self.user_id} "
            f"product_id={self.product_id} "
            f"quantity={self.quantity}>"
        )

class Basket(db.Model):
    tablename = "baskets"
    user = ForeignKey(User, nullable=False)
    product = ForeignKey(BasketItem, nullable=False)
    user_relationship = relationship("User", baskref="baskets")
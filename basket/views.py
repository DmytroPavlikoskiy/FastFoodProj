from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from db_config.db_manager import db
from basket.models import Basket, BasketItem
from menu.models import Dish

basket_bp = Blueprint("basket", __name__, template_folder="templates")

def get_or_create_basket():
    basket = Basket.query.filter_by(user_id=current_user.id).first()
    if not basket:
        basket = Basket(user_id=current_user.id)
        db.session.add(basket)
        db.session.commit()
    return basket

@basket_bp.route("/")
@login_required
def basket_detail():
    basket = get_or_create_basket()
    total_price = sum(item.dish.price * item.quantity for item in basket.items)
    return render_template("basket/basket.html", basket=basket, total_price=total_price)

@basket_bp.route("/add/<int:dish_id>")
@login_required
def basket_add_product(dish_id):
    basket = get_or_create_basket()
    item = BasketItem.query.filter_by(basket_id=basket.id, dish_id=dish_id).first()
    
    if item:
        item.quantity += 1
    else:
        item = BasketItem(basket_id=basket.id, dish_id=dish_id, quantity=1)
        db.session.add(item)
    
    db.session.commit()
    flash("Додано в кошик", "success")
    return redirect(request.referrer or url_for('menu.list_dishes'))

@basket_bp.route("/minus/<int:item_id>")
@login_required
def basket_minus_product(item_id):
    item = BasketItem.query.get_or_404(item_id)
    if item.quantity > 1:
        item.quantity -= 1
        db.session.commit()
    else:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('basket.basket_detail'))

@basket_bp.route("/remove/<int:item_id>")
@login_required
def basket_remove_product(item_id):
    item = BasketItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Товар видалено", "info")
    return redirect(url_for('basket.basket_detail'))

@basket_bp.route("/clear")
@login_required
def basket_clear():
    basket = get_or_create_basket()
    BasketItem.query.filter_by(basket_id=basket.id).delete()
    db.session.commit()
    flash("Кошик очищено", "warning")
    return redirect(url_for('basket.basket_detail'))
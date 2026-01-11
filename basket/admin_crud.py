from flask import Blueprint, render_template, redirect, url_for, flash
from basket.models import Basket, BasketItem
from db_config.db_manager import db
from flask_login import login_required
from db_config.decorators import admin_required

admin_basket_bp = Blueprint(
    "admin_basket",
    __name__,
    template_folder="templates"
)

# Список усіх активних кошиків
@admin_basket_bp.route("/baskets")
@login_required
@admin_required
def list_baskets():
    # Отримуємо всі кошики, де є хоча б один товар
    baskets = Basket.query.all()
    return render_template("admin_panel/baskets.html", baskets=baskets)

# Перегляд конкретного кошика
@admin_basket_bp.route("/baskets/<int:basket_id>")
@login_required
@admin_required
def view_basket(basket_id):
    basket = Basket.query.get_or_404(basket_id)
    return render_template("admin_panel/basket_details.html", basket=basket)

# Видалення позиції з кошика користувача (наприклад, якщо товару немає в наявності)
@admin_basket_bp.route("/baskets/item/delete/<int:item_id>", methods=["POST"])
@login_required
@admin_required
def delete_basket_item(item_id):
    item = BasketItem.query.get_or_404(item_id)
    basket_id = item.basket_id
    db.session.delete(item)
    db.session.commit()
    flash(f"Товар видалено з кошика", "warning")
    return redirect(url_for("admin_basket.view_basket", basket_id=basket_id))
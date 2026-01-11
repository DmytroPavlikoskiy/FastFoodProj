from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from db_config.db_manager import db
from basket.models import Basket, BasketItem
from orders.models import Order, OrderItem
from datetime import datetime

orders_bp = Blueprint('orders', __name__, template_folder="templates")

@orders_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    # 1. Знаходимо кошик користувача
    basket = Basket.query.filter_by(user_id=current_user.id).first()
    
    if not basket or not basket.items:
        flash("Ваш кошик порожній!", "warning")
        return redirect(url_for('menu.home_page'))

    # Розрахунок суми
    total_amount = sum(item.dish.price * item.quantity for item in basket.items)

    if request.method == 'POST':
        address = request.form.get('address')
        if not address:
            flash("Будь ласка, вкажіть адресу доставки", "danger")
            return render_template('orders/checkout.html', basket=basket, total=total_amount)

        # 2. Створюємо основне замовлення
        new_order = Order(
            user_id=current_user.id,
            total_amount=total_amount,
            delivery_address=address,
            status='pending'
        )
        db.session.add(new_order)
        db.session.flush() # Отримуємо ID замовлення перед комітом

        # 3. Переносимо товари з кошика в OrderItem
        for item in basket.items:
            order_item = OrderItem(
                order_id=new_order.id,
                dish_id=item.dish_id,
                quantity=item.quantity,
                price_at_time=item.dish.price # Фіксуємо ціну!
            )
            db.session.add(order_item)
            db.session.delete(item) # Видаляємо з кошика

        db.session.commit()
        return redirect(url_for('payment.process_payment', order_id=new_order.id))

    return render_template('orders/checkout.html', basket=basket, total=total_amount)


@orders_bp.route('/my-orders')
@login_required
def my_orders():
    # Отримуємо замовлення користувача, від нових до старих
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders/my_orders_list.html', orders=orders)
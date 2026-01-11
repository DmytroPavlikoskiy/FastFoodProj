from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required, current_user
from db_config.db_manager import db
from payment.models import Payment
from orders.models import Order
import uuid

payment_bp = Blueprint('payment', __name__, template_folder="templates")

@payment_bp.route('/process/<int:order_id>')
@login_required
def process_payment(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        abort(403)

    # Перевіряємо, чи вже існує платіж для цього замовлення
    payment = Payment.query.filter_by(order_id=order.id).first()
    
    if not payment:
        # Якщо платежу немає — створюємо "заглушку"
        payment = Payment(
            order_id=order.id,
            status="pending", 
            transaction_id=f"CASH-{uuid.uuid4().hex[:8].upper()}" # Додано літеру 'a'
        )
        db.session.add(payment)
        db.session.commit()
    
    # Якщо платіж вже був успішний, просто йдемо далі
    return redirect(url_for('payment.success_page', order_id=order.id))

@payment_bp.route('/success/<int:order_id>')
@login_required
def success_page(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('payment/success_thanks_for_bye.html', order=order)
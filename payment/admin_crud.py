from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from db_config.decorators import admin_required
from db_config.db_manager import db
from payment.models import Payment
from orders.models import Order

admin_payments_bp = Blueprint(
    "admin_payments",
    __name__,
    template_folder="templates"
)

@admin_payments_bp.route("/payments")
@login_required
@admin_required
def list_payments():
    # Отримуємо всі платежі, найновіші спочатку
    payments = Payment.query.order_by(Payment.id.desc()).all()
    return render_template("admin_panel/payments.html", payments=payments)

@admin_payments_bp.route("/payments/confirm/<int:payment_id>", methods=["POST"])
@login_required
@admin_required
def confirm_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    payment.status = "success"
    
    # Також можна автоматично змінити статус замовлення на "cooking"
    order = Order.query.get(payment.order_id)
    if order:
        order.status = "cooking"
    
    db.session.commit()
    flash(f"Платіж по замовленню #{payment.order_id} підтверджено", "success")
    return redirect(url_for("admin_payments.list_payments"))

@admin_payments_bp.route("/payments/fail/<int:payment_id>", methods=["POST"])
@login_required
@admin_required
def fail_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    payment.status = "failed"
    db.session.commit()
    flash(f"Платіж #{payment_id} відхилено", "danger")
    return redirect(url_for("admin_payments.list_payments"))
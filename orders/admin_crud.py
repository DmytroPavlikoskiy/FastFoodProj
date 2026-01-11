from flask import Blueprint, render_template, redirect, url_for, flash, request
from orders.models import Order, db
from db_config.decorators import admin_required
from flask_login import login_required
from datetime import datetime

admin_orders_bp = Blueprint(
    "admin_orders",
    __name__,
    template_folder="templates"
)

@admin_orders_bp.route("/orders")
@login_required
@admin_required
def list_orders():
    # Отримуємо всі замовлення, найновіші зверху
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin_panel/orders.html", orders=orders)

@admin_orders_bp.route("/orders/<int:order_id>")
@login_required
@admin_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template("admin_panel/order_detail.html", order=order)

@admin_orders_bp.route("/orders/update_status/<int:order_id>", methods=["POST"])
@login_required
@admin_required
def update_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get("status")
    
    # Список дозволених статусів
    valid_statuses = ["pending", "cooking", "on_the_way", "delivered", "cancelled"]
    
    if new_status in valid_statuses:
        order.status = new_status
        db.session.commit()
        flash(f"Статус замовлення #{order.id} оновлено на {new_status}", "success")
    else:
        flash("Некоректний статус", "danger")
        
    return redirect(url_for("admin_orders.order_detail", order_id=order.id))
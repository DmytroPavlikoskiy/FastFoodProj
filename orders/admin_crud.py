from flask import Blueprint, render_template
from .models import Order

admin_bp = Blueprint(
    "admin",
    __name__,
    template_folder="templates"
)

@admin_bp.route("/admin/orders")
def admin_orders():
    orders = Order.query.all()
    return render_template("admin_orders.html", orders=orders)

@admin_bp.route("/admin/orders/<int:order_id>")
def admin_order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template("admin_order_detail.html", order=order)
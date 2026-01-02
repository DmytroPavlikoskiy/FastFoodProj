from flask import Blueprint

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/example_url')
def example():
    pass
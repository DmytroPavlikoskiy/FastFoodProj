from flask import Blueprint

basket_bp = Blueprint('basket', __name__)

@basket_bp.route('/example_url')
def example():
    pass
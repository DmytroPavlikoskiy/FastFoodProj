from flask import Blueprint

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/example_url')
def example():
    pass
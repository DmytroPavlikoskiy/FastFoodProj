from flask import Blueprint

users_bp = Blueprint('users', __name__)

@users_bp.route('/example_url')
def example():
    pass
from flask import Blueprint, jsonify, request
from models import db, User
from flask import abort
from flask_login import current_user

admin_users_bp = Blueprint("admin", __name__)

def admin_required():
    if not current_user.is_authenticated or current_user.role != "admin":
        abort(403)


@admin_users_bp.route("/users", methods=["GET"])
def get_users():
    admin_required()

    users = User.query.all()
    return jsonify([
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "phone": u.phone,
            "address": u.address
        } for u in users
    ])

@admin_users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    admin_required()

    user = User.query.get_or_404(user_id)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "phone": user.phone,
        "address": user.address
    })


@admin_users_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    admin_required()

    user = User.query.get_or_404(user_id)
    data = request.json

    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    user.phone = data.get("phone", user.phone)
    user.address = data.get("address", user.address)
    user.role = data.get("role", user.role)

    db.session.commit()
    return jsonify({"message": "Роль змінено"})


@admin_users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    admin_required()

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Користувача видалено"})
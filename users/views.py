from flask import Blueprint, request, jsonify, render_template, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from db_config.db_manager import login_manager, db
from users.models import User
from db_config.db_manager import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for


users_bp = Blueprint('users', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@users_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("sign_in_sign_up.html")


@users_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    password_confirm = data.get("password_confirm")
    phone = data.get("phone")
    address = data.get("address")

    user = User()

    if user.get_user_by_email(email=email):
        return jsonify({"error": "Email вже існує"}), 400

    if user.get_user_by_username(username=username):
        return jsonify({"error": "Username вже існує"}), 400
    
    if password and password_confirm and password != password_confirm:
        return jsonify({"error": "Паролі не співпадають!"}), 400
    
    user, create = user.get_or_create(
        User,
        email=email,
        username=username,
        password_hash=generate_password_hash(password),
        phone=phone,
        address=address
    )
    if create:
        return jsonify({"message": "Реєстрація успішна"}), 201
    else:
        return jsonify({"message": "Упс, щось пішло не так !!!"}), 400


@users_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("sign_in_sign_up.html")

@users_bp.route("/login", methods=["POST"])
def login():
    # Якщо приходить JSON (через JS/Fetch)
    if request.is_json:
        data = request.json
        identifier = data.get("email") or data.get("username")
        password = data.get("password")
    else:
        # Якщо приходить звичайна HTML-форма
        identifier = request.form.get("email")
        password = request.form.get("password")

    if not identifier or not password:
        return jsonify({"error": "Не вистачає даних для входу!"}), 400

    # Шукаємо користувача за email АБО username
    user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()

    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        # Для API повертаємо JSON, для форми — redirect
        if request.is_json:
            return jsonify({"message": "Успішно"}), 200
        return redirect(url_for('menu.index')) # Змініть на ваш реальний endpoint
    
    return jsonify({"error": "Невірний логін або пароль"}), 401



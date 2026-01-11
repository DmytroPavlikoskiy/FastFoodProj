import os
from flask import Blueprint, request, jsonify, render_template, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Імпортуємо об'єкти з вашого проекту
from db_config.db_manager import login_manager, db
from users.models import User

users_bp = Blueprint('users', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- СТОРІНКИ (GET) ---

@users_bp.route("/register", methods=["GET"])
def register_page():
    # Оскільки у вас одна сторінка для входу та реєстрації
    return render_template("users/sign_in_sign_up.html")

@users_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("users/sign_in_sign_up.html")

# --- ЛОГІКА (POST) ---

@users_bp.route("/register", methods=["POST"])
def register():
    # Універсальне отримання даних (JSON або Form)
    if request.is_json:
        data = request.json
    else:
        data = request.form

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    password_confirm = data.get("password_confirm")
    phone = data.get("phone")
    address = data.get("address")

    # Перевірки
    user_helper = User()
    
    if not email or not username or not password:
        flash("Заповніть обов'язкові поля!", "danger")
        return redirect(url_for('users.register_page'))

    if user_helper.get_user_by_email(email=email):
        flash("Користувач з таким Email вже існує", "danger")
        return redirect(url_for('users.register_page'))

    if password != password_confirm:
        flash("Паролі не співпадають!", "danger")
        return redirect(url_for('users.register_page'))
    
    # Створення користувача через ваш метод get_or_create
    new_user, created = user_helper.get_or_create(
        User,
        email=email,
        username=username,
        password_hash=generate_password_hash(password),
        phone=phone,
        address=address
    )

    if created:
        login_user(new_user)
        flash("Реєстрація успішна! Ласкаво просимо.", "success")
        return redirect(url_for('menu.home_page'))
    else:
        flash("Помилка при створенні акаунту.", "danger")
        return redirect(url_for('users.register_page'))


@users_bp.route("/login", methods=["POST"])
def login():
    # Отримуємо дані (email може бути як email, так і username)
    identifier = request.form.get("email")
    password = request.form.get("password")

    if not identifier or not password:
        flash("Введіть логін та пароль", "warning")
        return redirect(url_for('users.login_page'))

    # Шукаємо користувача за email АБО username
    user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()

    # Перевірка хешу пароля
    if user and check_password_hash(user.password_hash, password):
        login_user(user, remember=request.form.get("remember"))
        flash(f"Раді бачити, {user.username}!", "success")
        
        # Перенаправлення на головну сторінку меню
        return redirect(url_for('menu.home_page'))
    
    # Якщо дані невірні
    flash("Невірний email/username або пароль", "danger")
    return redirect(url_for('users.login_page'))

@users_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Ви вийшли з системи", "info")
    return redirect(url_for('users.login_page'))


@users_bp.route("/profile")
@login_required
def profile():
    # Перевіряємо, чи є у користувача профіль (якщо немає - створюємо порожній)
    if not current_user.profile:
        from users.models import Profile
        new_profile = Profile(user_id=current_user.id)
        db.session.add(new_profile)
        db.session.commit()
    
    return render_template("users/profile.html", user=current_user)
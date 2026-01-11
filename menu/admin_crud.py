import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from db_config.decorators import admin_required
from db_config.db_manager import db
from menu.models import Dish, Category

admin_menu_bp = Blueprint("admin_menu", __name__, template_folder="templates")

@admin_menu_bp.route('/menu_manager')
@login_required
@admin_required
def menu_manager():
    dishes = Dish.query.all()
    categories = Category.query.all()
    return render_template("admin_panel/menu_manager.html", dishes=dishes, categories=categories)

@admin_menu_bp.route('/add_dish', methods=["POST"])
@login_required
@admin_required
def add_dish():
    name = request.form.get('name')
    price = request.form.get('price')
    category_id = request.form.get('category_id')
    file = request.files.get('image')

    if file and name and price:
        filename = secure_filename(file.filename)
        # Створюємо папку, якщо її немає
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'dishes')
        os.makedirs(upload_path, exist_ok=True)
        
        file.save(os.path.join(upload_path, filename))
        
        db_path = f"images/dishes/{filename}" # шлях для static
        
        new_dish = Dish(
            name=name,
            price=float(price),
            image_url=db_path,
            category_id=int(category_id) if category_id else None
        )
        db.session.add(new_dish)
        db.session.commit()
        flash("Страву додано!", "success")
    
    return redirect(url_for('admin_menu.menu_manager'))

@admin_menu_bp.route('/delete_dish/<int:dish_id>', methods=["POST"])
@login_required
@admin_required
def delete_dish(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    # Можна також додати видалення файлу з сервера тут
    db.session.delete(dish)
    db.session.commit()
    flash("Страву видалено", "danger")
    return redirect(url_for('admin_menu.menu_manager'))

# Додатково: Керування категоріями
@admin_menu_bp.route('/add_category', methods=["POST"])
@login_required
@admin_required
def add_category():
    name = request.form.get('name')
    if name:
        new_cat = Category(name=name)
        db.session.add(new_cat)
        db.session.commit()
        flash("Категорію створено", "success")
    return redirect(url_for('admin_menu.menu_manager'))
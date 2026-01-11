from flask import Blueprint, render_template, request
from flask_login import login_required
from db_config.db_manager import db
from menu.models import Dish, Category

menu_bp = Blueprint('menu', __name__, template_folder="templates")

@menu_bp.route('/')
@login_required
def home_page():
    # Отримуємо параметри пошуку та категорії
    search_query = request.args.get('q', '')
    category_id = request.args.get('category_id', type=int)
    
    categories = Category.query.all()
    
    # Базовий запит
    query = Dish.query
    
    # Фільтрація за пошуковим словом
    if search_query:
        query = query.filter(Dish.name.ilike(f'%{search_query}%'))
        
    # Фільтрація за категорією
    if category_id:
        query = query.filter_by(category_id=category_id)
        active_category = Category.query.get(category_id)
    else:
        active_category = None

    dishes = query.all()

    return render_template(
        "menu/home_page.html", 
        categories=categories, 
        dishes=dishes, 
        active_category=active_category,
        search_query=search_query # Передаємо назад, щоб заповнити поле пошуку
    )
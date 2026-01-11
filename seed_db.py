import os
from main import app  # Імпортуємо твій об'єкт Flask
from db_config.db_manager import db
from menu.models import Category, Dish

def seed_data():
    with app.app_context():
        print("🚀 Починаємо заповнення бази даних...")

        # 1. Створюємо категорії
        categories_data = ["Бургери", "Піца", "Напої"]
        categories_objs = {}

        for cat_name in categories_data:
            category = Category.query.filter_by(name=cat_name).first()
            if not category:
                category = Category(name=cat_name)
                db.session.add(category)
                db.session.commit()
                print(f"✅ Категорія '{cat_name}' створена.")
            categories_objs[cat_name] = category

        # 2. Створюємо страви
        # Шлях вказуємо відносно папки static, щоб url_for('static', filename=...) працював
        dishes_data = [
            {
                "name": "Яловичий Бургер",
                "price": 150.0,
                "image": "images/dishes/Beef_burger.png",
                "cat": "Бургери"
            },
            {
                "name": "Чікен Бургер",
                "price": 135.0,
                "image": "images/dishes/Chicken_burger.png",
                "cat": "Бургери"
            },
            {
                "name": "Піца Пепероні",
                "price": 220.0,
                "image": "images/dishes/Paperoni.png",
                "cat": "Піца"
            },
            {
                "name": "Піца 4 Сири",
                "price": 240.0,
                "image": "images/dishes/four_chees.png",
                "cat": "Піца"
            },
            {
                "name": "Гавайська Піца",
                "price": 210.0,
                "image": "images/dishes/havai.png",
                "cat": "Піца"
            }
        ]

        for item in dishes_data:
            existing_dish = Dish.query.filter_by(name=item["name"]).first()
            if not existing_dish:
                new_dish = Dish(
                    name=item["name"],
                    price=item["price"],
                    image_url=item["image"],
                    category_id=categories_objs[item["cat"]].id
                )
                db.session.add(new_dish)
                print(f"🍔 Страва '{item['name']}' додана.")
            else:
                print(f"⚠️ Страва '{item['name']}' вже є в базі.")

        db.session.commit()
        print("✨ Заповнення завершено успішно!")

if __name__ == "__main__":
    seed_data()
#db_config/db_manager.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()

class Base(DeclarativeBase):
    pass

# Ініціалізуємо об'єкти
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

def init_db(app):
    # Отримуємо дані з .env або ставимо дефолтні
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "1111")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    name = os.getenv("POSTGRES_NAME", "fastfood_db")

    # Формуємо URL підключення
    database_conf = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'
    
    # 1. Спершу налаштовуємо конфіг в app
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', database_conf)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 2. Потім ініціалізуємо db з цим app
    db.init_app(app)

    # 3. Створюємо таблиці в контексті додатка
    with app.app_context():
        try:
            # 1. Імпортуємо ВСІ моделі з проекту
            from users.models import User, Profile 
            from menu.models import Category, Dish, Comments
            from basket.models import Basket, BasketItem
            from payment.models import Payment
            from orders.models import Order, OrderItem
            # Додай інші, якщо вони є (наприклад, Comments)

            # 2. Тепер створюємо таблиці
            db.create_all()
            print(f"✅ База даних '{name}' та таблиці успішно перевірені!")
        except Exception as e:
            print(f"❌ Помилка ініціалізації БД: {e}")
    # with app.app_context():
    #     try:
    #         # Імпортуємо моделі тут, щоб SQLAlchemy знала про них
    #         from users.models import User, Profile 
    #         db.create_all()
    #         print(f"✅ База даних '{name}' та таблиці успішно перевірені!")
    #     except Exception as e:
    #         print(f"❌ Помилка ініціалізації БД: {e}")


def get_db():
    return db
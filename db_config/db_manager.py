from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv
#Незабудьте імпортувати сюди ваші моделі з файла наприклад users/models.py
#from users.models import User, Profile ...

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST=os.getenv("POSTGRES_HOST")
POSTGRES_PORT=os.getenv("POSTGRES_PORT")
POSTGRES_NAME=os.getenv("POSTGRES_NAME")

# Створюємо базовий клас для моделей (для SQLAlchemy 3.x)
class Base(DeclarativeBase):
    pass

# Ініціалізуємо об'єкт БД
db = SQLAlchemy(model_class=Base)

def init_db(app):
    # Збираємо рядок, але додаємо захист: якщо змінна None, ставимо пустий рядок або дефолт
    user = POSTGRES_USER or 'postgres'
    password = POSTGRES_PASSWORD or '1111'
    host = POSTGRES_HOST or 'localhost'
    port = POSTGRES_PORT or '5432'
    name = POSTGRES_NAME or 'fastfood_db'

    database_conf = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'
    
    # Пріоритет: 1. DATABASE_URL з середовища, 2. Наш зібраний рядок
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', database_conf)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        # ВАЖЛИВО: Тут мають бути імпортовані моделі всіх груп, 
        # щоб SQLAlchemy їх "побачила" перед створенням.
        # Наприклад: from users.models import User
        
        try:
            db.create_all()
            print(f"✅ Підключено до БД: {name}")
            print("✅ Всі таблиці PostgreSQL успішно перевірені/створені!")
        except Exception as e:
            print(f"❌ Помилка ініціалізації БД: {e}")
def get_db():
    """Допоміжний метод для отримання сесії (якщо знадобиться)"""
    return db
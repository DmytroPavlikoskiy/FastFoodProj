import os
from flask import Flask
from db_config.db_manager import init_db
from dotenv import load_dotenv

# Завантажуємо змінні з .env (SECRET_KEY тощо)
load_dotenv()

app = Flask(__name__)

# --- МІНІМАЛЬНА БЕЗПЕКА ТА НАЛАШТУВАННЯ ---
# Секретний ключ для сесій та CSRF-захисту (обов'язково для форм)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-12345')

# Налаштування завантаження файлів (для картинок меню)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Ліміт 16 МБ на завантаження
app.config['UPLOAD_FOLDER'] = 'static/images'

# --- ІНІЦІАЛІЗАЦІЯ БАЗИ ДАНИХ ---
init_db(app)

# --- РЕЄСТРАЦІЯ BLUEPRINTS (Як це має бути) ---
# Діти створюють їх у своїх папках, а ви тут імпортуєте
try:
    from users.views import users_bp
    app.register_blueprint(users_bp, url_prefix='/users')
    
    from menu.views import menu_bp
    app.register_blueprint(menu_bp, url_prefix='/menu')
    
    from basket.views import basket_bp
    app.register_blueprint(basket_bp, url_prefix='/basket')
    
    from orders.views import orders_bp
    app.register_blueprint(orders_bp, url_prefix='/orders')
    
    from payment.views import payment_bp
    app.register_blueprint(payment_bp, url_prefix='/payment')
    
    print("✅ Усі модулі (Blueprints) успішно зареєстровані!")
except ImportError as e:
    print(f"⚠️ Помилка імпорту модулів: {e}")

@app.route('/')
def index():
    return {"message": "Welcome to FastFood API", "status": "running"}

if __name__ == "__main__":
    app.run(debug=True, port=5000)
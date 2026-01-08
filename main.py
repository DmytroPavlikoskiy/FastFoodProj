import os
from flask import Flask, url_for
from dotenv import load_dotenv

# Імпортуємо вже створені об'єкти з твого менеджера
from db_config.db_manager import db, login_manager, init_db

# 1. Завантажуємо змінні оточення
load_dotenv()

app = Flask(__name__)

# 2. Конфігурація додатка
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-12345')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'static/images'

# 3. Ініціалізація розширень
# Прив'язуємо login_manager, який ми створили в db_manager.py
login_manager.init_app(app)
login_manager.login_view = 'users.login_page'

# 4. Ініціалізація бази даних (з контекстом додатка всередині)
init_db(app)

# 5. Реєстрація Blueprints
# Робимо імпорт тут, щоб уникнути circular imports
try:
    from users.views import users_bp
    app.register_blueprint(users_bp, url_prefix='/users')
    

    
    print("✅ Усі модулі (Blueprints) успішно зареєстровані!")
except Exception as e:
    print(f"❌ Помилка при реєстрації Blueprints: {e}")


@app.route('/')
def index():
    return {"message": "Welcome to FastFood API", "status": "running"}


if __name__ == "__main__":
    # Виводимо всі доступні URL для перевірки 404
    with app.app_context():
        print("\n" + "="*30)
        print("ЗАРЕЄСТРОВАНІ МАРШРУТИ:")
        for rule in app.url_map.iter_rules():
            # rule.endpoint — це назва функції, rule — це сам шлях
            print(f"🔹 {rule.endpoint: <25} -> {rule}")
        print("="*30 + "\n")
    
    app.run(debug=True, port=5000)


# --- РЕЄСТРАЦІЯ BLUEPRINTS (Як це має бути) ---
# Діти створюють їх у своїх папках, а ви тут імпортуєте
# try:
#     from users.admin_crud import admin_users_bp
#     app.register_blueprint(admin_users_bp, url_prefix='/admin/users')

#     from users.views import users_bp
#     app.register_blueprint(users_bp, url_prefix='/users')
    
#     from menu.views import menu_bp
#     app.register_blueprint(menu_bp, url_prefix='/menu')
    
#     from basket.views import basket_bp
#     app.register_blueprint(basket_bp, url_prefix='/basket')
    
#     from orders.views import orders_bp
#     app.register_blueprint(orders_bp, url_prefix='/orders')
    
#     from payment.views import payment_bp
#     app.register_blueprint(payment_bp, url_prefix='/payment')
    
#     print("✅ Усі модулі (Blueprints) успішно зареєстровані!")

# except ImportError as e:
#     print(f"⚠️ Помилка імпорту модулів: {e}")

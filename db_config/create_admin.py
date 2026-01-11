#db_config/create_admin.py
from main import app
from users.models import db, User
from werkzeug.security import generate_password_hash

def create_super_admin():
    with app.app_context():
        # Перевіряємо, чи вже є такий користувач
        admin = User.get_user_by_email(email="admin@fastfood.com")
        if not admin:
            new_admin, created = User.get_or_create(
                username="SuperAdmin",
                email="admin@fastfood.com",
                password=generate_password_hash("strong_password123"), # Не забудьте хешувати!
                role="admin"
            )
            if created:
                print("✅ Адміністратора успішно створено!")
        else:
            print("⚠️ Такий адмін вже існує.")

if __name__ == "__main__":
    create_super_admin()
from flask_login import UserMixin
from db_config.db_manager import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), default="client")
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)

    # Зв'язки
    profile = db.relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    orders = db.relationship("Order", backref="customer", lazy=True)
    basket = db.relationship("Basket", back_populates="user", uselist=False)

    # --- МЕТОДИ ДЛЯ РОБОТИ З ДАНИМИ ---

    @classmethod
    def get_user_by_email(cls, email):
        """Шукає користувача за email"""
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_user_by_username(cls, username):
        """Шукає користувача за ім'ям"""
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def get_or_create(model_class, **kwargs):
        """
        Метод для створення користувача, якщо його ще не існує.
        Повертає (об'єкт, створено_чи_ні)
        """
        # Перевіряємо за email (або іншим унікальним полем)
        instance = db.session.query(model_class).filter_by(email=kwargs.get('email')).first()
        if instance:
            return instance, False
        else:
            instance = model_class(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance, True

class Profile(db.Model):
    __tablename__ = "user_profiles"
    
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    user = db.relationship("User", back_populates="profile")
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_config.db_manager import db
from db_config.base_models import OurBase

class User(db.Model, UserMixin, OurBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False) # Збільшено довжину для сучасних хешів
    role = Column(String(10), default="client")
    phone = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)

    # Зв'язок 1-до-1 з профілем
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")

    # Методи пошуку (використовуємо @classmethod для зручного виклику User.get_by_...)
    @classmethod
    def get_user_by_id(cls, user_id):
        return cls.query.get(int(user_id))
          
    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first() if email else None

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first() if username else None

class Profile(db.Model): # UserMixin тут не потрібен, він тільки для класу User
    __tablename__ = "user_profile"
    
    id = Column(Integer, primary_key=True)
    avatar = Column(String(255), nullable=True) # Приклад додаткового поля
    
    # ПРАВИЛЬНИЙ ForeignKey: вказуємо рядок "назва_таблиці.стовпчик"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Зворотний зв'язок до користувача
    user = relationship("User", back_populates="profile")
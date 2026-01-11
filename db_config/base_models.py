#db_config/base_models.py
from db_config.db_manager import get_db

db = get_db()

class OurBase:
    @staticmethod
    def get_or_create(model, **kwargs):
        instance = db.session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance, False
        
        instance = model(**kwargs)
        try:
            db.session.add(instance)
            db.session.commit()
            return instance, True
        except Exception:
            db.session.rollback()
            return None, False
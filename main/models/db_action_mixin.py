from main.db import db


class DBActionMixin:
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    @staticmethod
    def save_to_db(obj):
        db.session.add(obj)
        db.session.commit()

    @staticmethod
    def delete_from_db(obj):
        db.session.delete(obj)
        db.session.commit()

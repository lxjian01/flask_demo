import datetime

from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_code = db.Column(db.String(64), nullable=False, unique=True, index=True)
    create_user = db.Column(db.String(64))
    create_at = db.Column(db.DateTime, default=datetime.datetime.now())
    update_user = db.Column(db.String(64))
    update_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

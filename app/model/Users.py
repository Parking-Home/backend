from app import db
from datetime import datetime


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=True, unique=True)
    firstname = db.Column(db.String(45), nullable=True)
    lastname = db.Column(db.String(45), nullable=True)
    telephone = db.Column(db.String(11), nullable=True, unique=True)
    email = db.Column(db.String(50), nullable=True, unique=True)
    age = db.Column(db.Integer, nullable=True)
    password = db.Column(db.String(255), nullable=True)
    registration_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<users {self.id}>"

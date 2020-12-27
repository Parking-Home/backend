from app import db
from datetime import datetime


class Users(db.Model):
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    telephone = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String, nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, id, username, firstname, lastname, telephone, email, age, password):
        self.id = id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.telephone = telephone
        self.email = email
        self.age = age
        self.password = password

    def __repr__(self):
        return f"<users {self.id}>"

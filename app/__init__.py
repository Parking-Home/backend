from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from app import views
from app.model import Notifications, Offers, ParkingPlaces, Reservation, Users

if __name__ == '__main__':
    app.run()

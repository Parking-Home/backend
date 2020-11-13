from app import db
from datetime import datetime, timedelta


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reservation_due = db.Column(db.DateTime, default=(datetime.now() + timedelta(hours=1)))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    parking_place_id = db.Column(db.Integer, db.ForeignKey('parking_places.id'))

    def __repr__(self):
        return f"<reservation{self.id}>"

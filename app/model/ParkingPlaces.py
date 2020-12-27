from app import db


class ParkingPlaces(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_free = db.Column(db.Boolean, nullable=False)
    # longitude = db.Column(db.Float, nullable=False)
    # latitude = db.Column(db.Float, nullable=False)

    def __init__(self, is_free):
        self.is_free = is_free

    def __repr__(self):
        return f"<ParkingPlaces {self.id}>"

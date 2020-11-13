from app import db


class ParkingPlaces(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<ParkingPlaces {self.id}>"

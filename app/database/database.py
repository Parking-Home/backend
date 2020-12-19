from app import db
from app.model.Notifications import Notifications
from app.model.Offers import Offers
from app.model.ParkingPlaces import ParkingPlaces
from app.model.Reservation import Reservation
from app.model.Users import Users


def get_data_for_reserve(req):
    user_id = req.get("session").get("user_id")
    for entity in req.get("request").get("nlu").get("entities"):
        if entity.get("type") == "YANDEX.NUMBER":
            parking_place = entity.get("value")
        if entity.get("type") == "YANDEX.DATETIME":
            dt = entity.get("value")
    return parking_place, dt, user_id


def reserve_place(req):
    parking_place, dt, user_id = get_data_for_reserve(req)
    # reservation = Reservation(dt, user_id, parking_place)
    # db.session.add(reservation)
    return parking_place, dt, user_id

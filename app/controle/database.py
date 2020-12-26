from app import db
from app.model.Notifications import Notifications
from app.model.Offers import Offers
from app.model.ParkingPlaces import ParkingPlaces
from app.model.Reservation import Reservation
from app.model.Users import Users


def get_data_for_reserve(req):
    is_got_parking_place = False
    is_got_dt = False
    user_id = req.get("session").get("user_id")
    for entity in req.get("request").get("nlu").get("entities"):
        if entity.get("type") == "YANDEX.NUMBER":
            parking_place = entity.get("value")
            is_got_parking_place = True
        if entity.get("type") == "YANDEX.DATETIME":
            dt = entity.get("value")
            is_got_dt = True
    if not is_got_parking_place:
        parking_place = None
    if not is_got_dt:
        raise KeyError
    return parking_place, dt, user_id

def reserve_place(req):
    parking_place, dt, user_id = get_data_for_reserve(req)
    # reservation = Reservation(dt, user_id, parking_place)
    # db.session.add(reservation)
    return parking_place, dt, user_id
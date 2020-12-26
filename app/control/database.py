from app import db
from app.model.Notifications import Notifications
from app.model.Offers import Offers
from app.model.ParkingPlaces import ParkingPlaces
from app.model.Reservation import Reservation
from app.model.Intents import Intents
from app.model.Users import Users


def reserve_place(user_id, id, dt):
    reservation = Reservation(dt, user_id, id)
    db.session.add(reservation)
    db.session.commit()


def make_intent(user_id, place, dt, intent):
    new_intent = Intents(user_id=user_id, intent=intent, dt=dt, place=place)
    db.session.add(new_intent)
    db.session.commit()


def get_intent(user_id):
    return Intents.query.filter_by(user_id=user_id)


def delete_intent(user_id):
    if Intents.query.filter_by(user_id=user_id) is not None:
        Intents.query.filter_by(user_id=user_id).delete()


def get_place():
    return ParkingPlaces.query.filter_by(is_Free=1).first().id

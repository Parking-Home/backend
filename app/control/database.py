# coding: utf-8
from app import db
from app.model.Notifications import Notifications
from app.model.Offers import Offers
from app.model.ParkingPlaces import ParkingPlaces
from app.model.Reservation import Reservation
from app.model.Intents import Intents
from app.model.Users import Users


def reserve_place(user_id, place_id, dt):
    place = ParkingPlaces.query.filter_by(id=place_id).first()
    place.is_free = 0
    reservation = Reservation(dt, user_id, place_id)
    db.session.add(reservation)
    db.session.commit()


def make_intent(user_id, place, dt, intent):
    new_intent = Intents(user_id=user_id, intent=intent, dt=dt, place=place)
    db.session.add(new_intent)
    db.session.commit()


def get_intent(user_id):
    return Intents.query.filter_by(user_id=user_id)


def get_free_place():
    return ParkingPlaces.query.filter_by(is_free=1).first().id


def has_user_reserved_place(user_id):
    return Reservation.query.filter_by(user_id=user_id).count() != 0


def get_reserved_place(user_id):
    return Reservation.query.filter_by(user_id=user_id).first().parking_place_id


def refresh_reservation(user_id, dt):
    reservation = Reservation.query.filter_by(user_id=user_id).first()
    reservation.reservation_due = dt
    db.session.commit()


def delete_reservation(user_id):
    res = Reservation.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return res


def is_authorized(user_id):
    return Users.query.filter_by(id=user_id).count() != 0


def create_new_user(user_id):
    user = Users(user_id, user_id, user_id, user_id, user_id, user_id, 18, user_id)
    db.session.add(user)
    db.session.commit()


def initialize_db():
    for i in range(20):
        place = ParkingPlaces(1)
        db.session.add(place)
    db.session.commit()
    print("added")


def refresh_time_intent(user_id, dt):
    intent = Intents.query.filter_by(user_id=user_id).first()
    intent.dt = dt
    db.session.commit()


def refresh_place_intent(user_id, place_id):
    intent = Intents.query.filter_by(user_id=user_id).first()
    intent.place = place_id
    db.session.commit()


def delete_intent(user_id):
    Intents.query.filter_by(user_id=user_id).delete()
    db.session.commit()


def is_free_place(place_id):
    return ParkingPlaces.query.filter_by(id=place_id).first().is_free == 1


def make_place_free(place_id):
    ParkingPlaces.query.filter_by(id=place_id).first().is_free = 1
    db.session.commit()

def has_free_places():
    return ParkingPlaces.query.filter_by(is_free=1).count() != 0

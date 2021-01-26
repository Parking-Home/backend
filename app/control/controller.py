# coding: utf-8

from datetime import time, datetime
from app.control import database
from app.control import responses
from app.model.Intents import Intents
from app import db
import sys

orig_stdout = sys.stdout

def book_place_handler(req):
    if not database.has_free_places():
        return responses.no_free_places(req)
    slots = req.get("request").get("nlu").get("intents").get("book_place").get("slots")
    user_id = req.get("session").get("user_id")
    place_id = None
    dt = None

    for slot_key, slot_value in slots.items():
        with open("/var/www/webApp/ParkingAtHome/log.txt", "a") as file_object:
            sys.stdout = file_object
            print(slots)
            sys.stdout = orig_stdout
        if slot_key == "id":
            place_id = slot_value.get("value")
        if slot_key == "dt":
            dtValueDict = slot_value.get("value")

            tempMin = None
            if ("minute" in dtValueDict):
                if ("minute_is_relative" in dtValueDict and dtValueDict.get("minute_is_relative")):
                    tempMin = datetime.now().minute + dtValueDict.get("minute")
                else:
                    tempMin = dtValueDict.get("minute")
            else:
                tempMin = datetime.now().minute

            tempHour = None
            if ("hour" in dtValueDict):
                if ("hour_is_relative" in dtValueDict and dtValueDict.get("hour_is_relative")):
                    tempHour = datetime.now().hour + dtValueDict.get("hour")
                else:
                    tempHour = dtValueDict.get("hour")
            else:
                tempHour = datetime.now().hour

            tempDay = None
            if ("day" in dtValueDict):
                if ("day_is_relative" in dtValueDict and dtValueDict.get("day_is_relative")):
                    tempDay = datetime.now().day + dtValueDict.get("day")
                else:
                    tempDay = dtValueDict.get("day")
            else:
                tempDay = datetime.now().day

            t = time(hour=tempHour, minute=tempMin)
            dt = datetime.combine(date=datetime(datetime.now().year, datetime.now().month, tempDay), time=t)

    if (place_id is not None) and (not database.is_free_place(place_id)):
        return responses.place_reserved_response(req)

    if (place_id is not None) and (dt is not None):
        if database.is_free_place(place_id):
            
            database.make_intent(user_id, place_id, dt, "book_place")
            return responses.make_confirmation_response(req, place_id, dt)
        else:
            return responses.place_reserved_response(req)

    elif (place_id is None) and (dt is not None):
        database.make_intent(user_id, place_id, dt, "book_place")
        return responses.choose_place_response(req)

    else:
        database.make_intent(user_id, place_id, dt, "book_place")
        return responses.choose_dt_response(req)


def confirm_handler(req):
    user_id = req.get("session").get("user_id")
    intent = database.get_intent(user_id=user_id).first()
    with open("/var/www/webApp/ParkingAtHome/log.txt", "a") as file_object:
        sys.stdout = file_object
        print("Intent: " + intent.intent)
        sys.stdout = orig_stdout
    if (intent.dt is not None) and (intent.place is not None):
        if intent.intent == "book_place":
            database.reserve_place(intent.user_id, intent.place, intent.dt)
            reservedPlace = intent.place
            reservationTime = intent.dt
            database.delete_intent(user_id)
            return responses.reservation_success_response(req, reservedPlace, reservationTime)

        elif intent.intent == "extend_res":
            dt = datetime.combine(date=datetime.today(), time=intent.dt)
            database.refresh_reservation(user_id, dt)
            dt = intent.dt
            database.delete_intent(user_id)
            return responses.extend_success_response(req, dt)

    elif (intent.place is not None) and (intent.intent == "cancel_res"):
        database.delete_reservation(user_id)

        database.make_place_free(intent.place)
        with open("/var/www/webApp/ParkingAtHome/log.txt", "a") as file_object:
            sys.stdout = file_object
            print("Deleted reservation")
            sys.stdout = orig_stdout

        database.delete_intent(user_id)

        with open("/var/www/webApp/ParkingAtHome/log.txt", "a") as file_object:
            sys.stdout = file_object
            print("Deleted intent")
            sys.stdout = orig_stdout

        return responses.cancel_success_response(req)


def reject_handler(req):
    intent = database.get_intent(user_id=req.get("session").get("user_id"))
    intent = intent.intent
    database.delete_intent(user_id=req.get("session").get("user_id"))
    if intent == "book_place":
        return responses.cancel_reservation_response(req, "Бронирование")
    if intent == "extend_res":
        return responses.cancel_reservation_response(req, "Продление")
    if intent == "cancel_res":
        return responses.cancel_reservation_response(req, "Снятие брони")


def dt_handler(req):
    json_dt = req.get("request").get("nlu").get("intents").get("slots").get("dt")
    user_id = req.get("session").get("user_id")
    t = time(hour=json_dt.get("value").get("hour"), minute=json_dt.get("value").get("minute"))
    dt = datetime.combine(date=datetime.today(), time=t)

    intent = database.get_intent(user_id)
    place_id = intent.place

    database.refresh_time_intent(user_id, dt)
    if place_id is not None:
        return responses.make_confirmation_response(req, place_id, dt)
    else:
        return responses.choose_place_response(req)


def book_place_ch_place_handler(req):
    user_id = req.get("session").get("user_id")
    place_id = req.get("request").get("nlu").get("intents").get("book_place_ch_place").get("slots").get("id")
    intent = database.get_intent(user_id=user_id).first()
    dt = intent.dt

    if place_id.get("type") == "YANDEX.STRING":
        place_id = database.get_free_place()
    else:
        place_id = place_id.get("value")

    database.refresh_place_intent(user_id, place_id)
    return responses.make_confirmation_response(req, place_id, dt)


def extend_res_handler(req):
    user_id = req.get("session").get("user_id")

    if not database.has_user_reserved_place(user_id):
        return responses.no_reserved_place_resp(req)

    slots = req.get("request").get("nlu").get("intents").get("extend_res").get("slots")

    reserved_place = database.get_reserved_place(user_id)

    if slots.get("dt") is not None:
        t = time(slots.get("dt").get("value").get("hour"), slots.get("dt").get("value").get("minute"))
        dt = datetime.combine(date=datetime.today(), time=t)
        database.make_intent(user_id, reserved_place, dt, "extend_res")
        return responses.confirmation_extend_response(req, dt)
    else:
        dt = None
        database.make_intent(user_id, reserved_place, dt, "extend_res")
        return responses.choose_new_dt_response(req)


def cancel_res_handler(req):
    user_id = req.get("session").get("user_id")

    if not database.has_user_reserved_place(user_id):
        with open("/var/www/webApp/ParkingAtHome/log.txt", "a") as file_object:
            sys.stdout = file_object
            print("User has no reservations.")
            sys.stdout = orig_stdout
        return responses.no_reserved_place_resp(req)

    place_id = database.get_reserved_place(user_id)

    with open("/var/www/webApp/ParkingAtHome/log.txt", "a") as file_object:
        sys.stdout = file_object
        print("Place id:")
        print(place_id)
        sys.stdout = orig_stdout

    database.make_intent(user_id, place_id, None, "cancel_res")
    return responses.make_confirmation_response_res_cancel(req, place_id)


def initialising_handler(req):
    user_id = req.get("session").get("user_id")
    if not database.is_authorized(user_id):
        database.create_new_user(user_id)

    query = Intents.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    #database.initialize_db()
    return responses.no_intents_response(req)


def handle_intents(req):
    intents = req.get("request").get("nlu").get("intents")
    for intent in intents:
        if intent == "YANDEX.HELP":
            return responses.make_help_response(req)

        if intent == "YANDEX.CONFIRM":
            return confirm_handler(req)

        if intent == "YANDEX.REJECT":
            return reject_handler(req)

        elif intent == "book_place":
            return book_place_handler(req)

        elif intent == "dt":
            return dt_handler(req)

        elif intent == "book_place_ch_place":
            return book_place_ch_place_handler(req)

        elif intent == "extend_res":
            return extend_res_handler(req)
        elif intent == "cancel_res":
            return cancel_res_handler(req)
        elif intent == "free_spaces":
            return responses.no_functional_response(req)
        elif intent == "my_res":
            return responses.no_functional_response(req)
    return initialising_handler(req)


def handle_request(request):
    if request.is_json:
        req = request.get_json()
        res = handle_intents(req)
    else:
        res = responses.make_bad_response()
    return res

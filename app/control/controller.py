# coding: utf-8
from flask import make_response, jsonify
from datetime import time
from app.control import database
from app.control import responses
from app.model.Intents import Intents


def book_place_handler(req):
    slots = req.get("request").get("nlu").get("intents").get("book_place").get("slots")
    user_id = req.get("session").get("user_id")
    place_id = None
    dt = None

    for slot in slots:
        if slot == "id":
            place_id = slot.get("value")
        if slot == "dt":
            dt = time(hour=slot.get("value").get("hour"), minute=slot.get("value").get("minute"))

    database.make_intent(user_id, place_id, dt, "book_place")

    if (place_id is not None) and (dt is not None):
        return responses.make_confirmation_response(req, place_id, dt)

    elif (place_id is None) and (dt is not None):
        return responses.choose_place_response(req)

    else:
        return responses.choose_dt_response(req)


def confirm_handler(req):
    user_id = req.get("session").get("user_id")
    intent = database.get_intent(user_id=user_id)
    if (intent.dt is not None) and (intent.place is not None):
        if intent.intent == "book_place":
            database.reserve_place(intent.user_id, intent.place, intent.dt)
            database.delete_intent(user_id)
            return responses.reservation_success_response(req, intent.place, intent.dt)

        elif intent.intent == "extend_res":
            database.refresh_reservation(user_id, intent.dt)
            dt = intent.dt
            database.delete_intent(user_id)
            return responses.extend_success_response(req, dt)

        elif intent.intent == "cancel_res":
            database.delete_reservation(user_id)
            database.delete_intent(user_id)
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
    dt = time(hour=json_dt.get("value").get("hour"), minute=json_dt.get("value").get("minute"))

    intent = database.get_intent(user_id)
    place_id = intent.place
    intent = intent.intent

    database.delete_intent(user_id)
    database.make_intent(user_id, place_id, dt, intent)
    if place_id is not None:
        return responses.make_confirmation_response(req, place_id, dt)
    else:
        return responses.choose_place_response(req)


def book_place_ch_place_handler(req):
    user_id = req.get("session").get("user_id")
    place_id = req.get("request").get("nlu").get("intents").get("slots").get("id")
    intent = database.get_intent(user_id)
    dt = intent.dt
    intent = intent.intent

    if place_id.get("type") == "YANDEX.STRING":
        place_id = database.get_free_place()
    else:
        place_id = place_id.get("value")

    database.delete_intent(user_id)
    database.make_intent(user_id, place_id, dt, intent)
    return responses.make_confirmation_response(req, place_id, dt)


def extend_res_handler(req):
    user_id = req.get("session").get("user_id")

    if not database.has_user_reserved_place(user_id):
        return responses.no_reserved_place_resp(req)

    slots = req.get("request").get("nlu").get("intents").get("extend_res").get("slots")

    reserved_place = database.get_reserved_place(user_id)

    if slots.get("dt") is not None:
        dt = time(slots.get("dt").get("value").get("hour"), slots.get("dt").get("value").get("minute"))
        database.make_intent(user_id, reserved_place, dt, "extend_res")
        return responses.confirmation_extend_response(req, dt)
    else:
        dt = None
        database.make_intent(user_id, reserved_place, dt, "extend_res")
        return responses.choose_new_dt_response(req)


def cancel_res_handler(req):
    user_id = req.get("session").get("user_id")

    if not database.has_user_reserved_place(user_id):
        return responses.no_reserved_place_resp(req)

    place_id = database.get_reserved_place(user_id)

    database.make_intent(user_id, place_id, None, "cancel_res")


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
    return responses.no_intents_response(req)


def handle_request(request):
    if request.is_json:
        req = request.get_json()
        res = handle_intents(req)
    else:
        res = responses.make_bad_response()
    return res

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

    if (place_id is not None) and (dt is not None):
        database.make_intent(user_id, place_id, dt, "book_place")
        response = responses.make_confirmation_response(req, place_id, dt)
    return response


def confirm_handler(req):
    intent = database.get_intent(user_id=req.get("session").get("user_id"))
    if (intent.dt is not None) and (intent.place is not None):
        if intent.intent == "book_place":
            database.reserve_place(intent.user_id, intent.place, intent.dt)
            return responses.reservation_success_response(req, intent.place, intent.dt)


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


def handle_intents(req):
    intents = req.get("request").get("nlu").get("intents")
    for intent in intents:
        if intent == "YANDEX.HELP":
            return responses.make_help_response(req)

        if intent == "YANDEX.CONFIRM":
            return confirm_handler()

        if intent == "YANDEX.REJECT":
            return reject_handler()

        elif intent == "book_place":
            return book_place_handler(req)

        elif intent == "dt":
            return dt_handler(req)

        elif intent == "book_place_ch_place":
            return book_place_ch_place_handler()

        elif intent == "extend_res":
            return extend_res_handler()

        elif intent == "cancel_res":
            return cancel_res_handler()

        elif intent == "free_spaces":
            return free_spaces_handler()


def handle_request(request):
    if request.is_json:
        req = request.get_json()
        res = handle_intents(req)
    else:
        res = responses.make_bad_response()
    return res

from flask import make_response, jsonify


def make_bad_response():
    response = {
        "response": {
            "text": "Что-то пошло не так, перезапустите приложение и попробуйте ещё раз",
            "end_session": True
        },
        "version": "1.0"
    }
    return make_response(jsonify(response), 400)


def make_help_response(req):
    response = {
        "response": {
            "session": req.get("session"),
            "text": "Чтобы забронировать место, скажите 'Забронировать место', номер места и время\n"
                    "Чтобы продлить бронь, скажите 'Продлить бронь' и время\n"
                    "Чтобы снять бронь, скажите 'Снять бронь'\n"
                    "Чтобы получить информацию о своей брони, скажите 'Моя бронь'\n"
                    "Чтобы узнать, есть ли свободные места, скажите 'Свободные места'\n",
            "end_session": False
        },
        "version": req.get("version")
    }
    return make_response(jsonify(response), 200)


def reservation_success_response(req, place_id, dt):
    response = {
        "response": {
            "session": req.get("session"),
            "text": "Место " + str(place_id) + " забронировано до " + str(dt),
            "end_session": False
        },
        "version": req.get("version")
    }
    return make_response(jsonify(response), 200)


def make_confirmation_response(req, place_id, dt):
    response = {
        "response": {
            "session": req.get("session"),
            "text": "Забронировать место " + str(place_id) + " до " + str(dt) + "?",
            "end_session": False
        },
        "version": req.get("version")
    }
    return make_response(jsonify(response), 200)


def cancel_reservation_response(req, param):
    response = {
        "response": {
            "session": req.get("session"),
            "text": param + " отменено"
        }
    }
    return make_response(jsonify(response), 200)

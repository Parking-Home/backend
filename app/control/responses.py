# coding: utf-8
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
            "text": param + " отменено",
            "end_session": False
        },
        "version": req.get("version")
    }
    return make_response(jsonify(response), 200)


def choose_place_response(req):
    response = {
        "response": {
            "session": req.get("session"),
            "text": "Назовите номер места. Либо скажите 'любое'",
            "end_session": False
        },
        "version": req.get("version")
    }
    return make_response(jsonify(response), 200)


def choose_dt_response(req):
    response = {
        "response": {
            "session": req.get("session"),
            "text": "Назовите время окончания брони",
            "end_session": False
        },
        "version": req.get("version")
    }
    return make_response(jsonify(response), 200)


def no_intents_response(req):
    response = {
        "response": {
            "session": req.get("session"),
            "text": "Привет, я помогу забронировать парковочное место.\n"
                    "Назовите команду или скажите 'помощь', чтобы получить список доступных команд",
            "end_session": False
        },
        "version": req.get("version")
    }
    return make_response(jsonify(response), 200)


def no_functional_response(req):
    response = {
        "response": {
            "session": req.get("session"),
            "text": "К сожалению, данный функционал на этом этапе разработки ещё не доступен.\n"
                    "Наша команда разработчиков приносит свои глубочайшие извинения",
            "end_session": False
        },
        "version": req.get("version")
    }
    return make_response(jsonify(response), 200)


def no_reserved_place_resp(req):
    response = {
        "response": {
            "session": req.get("session"),
            "text": "У Вас нет забронированных мест",
            "end_session": False
        },
        "version": req.get("version")
    }
    return make_response(jsonify(response), 200)


def confirmation_extend_response(req, dt):
    response = {
        "response": {
            "session": req.get("session"),
            "text": "Продлить бронь до " + str(dt) + "?",
            "end_session": False
        },
        "version": req.get("version")
    }
    return make_response(jsonify(response), 200)


def choose_new_dt_response(req):
    response = {
        "response": {
            "session": req.get("session"),
            "text": "Назовите новое время окончания бронирования",
            "end_session": False
        },
        "version": req.get("version")
    }
    return make_response(jsonify(response), 200)


def extend_success_response(req, dt):
    response = {
        "response": {
            "session": req.get("session"),
            "text": "Бронь продлена до " + str(dt),
            "end_session": False
        },
        "version": req.get("version")
    }
    return make_response(jsonify(response), 200)


def cancel_success_response(req):
    response = {
        "response": {
            "session": req.get("session"),
            "text": "Ваша бронь снята",
            "end_session": False
        },
        "version": req.get("version")
    }
    return make_response(jsonify(response), 200)


def place_reserved_response(req):
    response = {
        "response": {
            "session": req.get("session"),
            "text": "К сожалению, данное место занято",
            "end_session": False
        },
        "version": req.get("version")
    }
    return make_response(jsonify(response), 200)


def no_free_places(req):
    response = {
        "response": {
            "session": req.get("session"),
            "text": "К сожалению, свободных мест нет",
            "end_session": False
        },
        "version": req.get("version")
    }
    return make_response(jsonify(response), 200)
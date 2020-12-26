from flask import make_response, jsonify
from app.controle import database


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


def handle_intents(req):
    intents = req.get("request").get("nlu").get("insets")
    for intent in intents:
        if intent == "YANDEX.HELP":
            return make_help_response(req)
        elif intent == "book_place":
            return make_bad_response()
        elif intent == "dt":
            return make_bad_response()
        elif intent == "book_place_ch_place":
            return make_bad_response()
        elif intent == "extend_res":
            return make_bad_response()
        elif intent == "cancel_res":
            return make_bad_response()
        elif intent == "free_spaces":
            return make_bad_response()


def handle_request(request):
    if request.is_json:
        req = request.get_json()
        res = handle_intents(req)
    else:
        res = make_bad_response()
    return res


    #     if req.get("request").get("original_utterance"):
    #         try:
    #             parking_place, dt, user_id = database.reserve_place(req)
    #             response = {
    #                 "response": {
    #                     "session": req.get("session"),
    #                     "text": "Запрос получен. Вы назвали следующие данные: dt = " + str(dt) + ", user_id = " + str(
    #                         user_id) + ", "
    #                                    "parking_place = " + str(parking_place),
    #                     "end_session": False
    #                 },
    #                 "version": req.get("version")
    #             }
    #         except KeyError:
    #             response = {
    #                 "session": req.get("session"),
    #                 "response": {
    #                     "text": "Пожалуйста, назовите время и место для парковки",
    #                     "end_session": False
    #                 },
    #                 "version": req.get("version")
    #             }
    #             return make_response(jsonify(response), 200)
    #     else:
    #         response = {
    #             "session": req.get("session"),
    #             "response": {
    #                 "text": "Назовите номер места и время брони",
    #                 "end_session": False
    #             },
    #             "version": req.get("version")
    #         }
    #     res = make_response(jsonify(response), 200)
    # else:
    #     res = make_bad_response()
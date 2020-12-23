from flask import render_template, flash, redirect, request, make_response, jsonify
from app import app
from app.database import database
from app.view.forms import LoginForm
from app.model.Users import Users
from app.model.Offers import Offers
from app.model.Notifications import Notifications
from app.model.ParkingPlaces import ParkingPlaces
from app.model.Reservation import Reservation
import json


def make_bad_response():
    response = {
        "response": {
            "text": "Что-то пошло не так, перезапустите приложение и попробуйте ещё раз",
            "end_session": True
        },
        "version": "1.0"
    }
    return make_response(jsonify(response), 400)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/posts')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@app.route('/api/web', methods=['POST'])
def api_web():
    if request.is_json:
        req = request.get_json()
        if req.get("request").get("original_utterance"):
            try:
                parking_place, dt, user_id = database.reserve_place(req)
                response = {
                    "response": {
                        "text": "Запрос получен. Вы назвали следующие данные: dt = " + str(dt) + ", user_id = " + str(
                            user_id) + ", "
                                       "parking_place = " + str(parking_place),
                        "end_session": False
                    },
                    "version": req.get("version")
                }
            except KeyError:
                response = {
                    "response": {
                        "text": "Пожалуйста, назовите время и место для парковки",
                        "end_session": False
                    },
                    "version": req.get("version")
                }
                return make_response(jsonify(response), 400)
        else:
            response = {
                "response": {
                    "text": "Назовите номер места и время брони",
                    "end_session": False
                },
                "version": req.get("version")
            }
        res = make_response(jsonify(response), 200)
    else:
        res = make_bad_response()
    return res


@app.route('/post', methods=['POST'])
def main():
    # Создаем ответ
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    # Заполняем необходимую информацию
    handle_dialog(response, request.json)
    return make_response(response, 200)


def handle_dialog(res, req):
    if req['request']['original_utterance']:
        # Проверяем, есть ли содержимое
        res['response']['text'] = req['request']['original_utterance']
    else:
        # Если это первое сообщение — представляемся
        res['response']['text'] = "Я echo-bot, повторяю за тобой"


@app.route('/')
def hello_world():
    return redirect('/post')


@app.route('/json', methods=["POST"])
def json():
    if request.is_json:
        req = request.get_json()
        response = {
            "message": "Json received",
            "name": req.get("name")
        }
        res = make_response(jsonify(response), 200)
    else:
        response = {
            "message": "Json wasn't received",
        }
        res = make_response(jsonify(response), 400)
    return res


@app.route('/home')
def index():
    user = {'nickname': 'Miguel'}  # выдуманный пользователь
    return render_template("index.html", user=user)

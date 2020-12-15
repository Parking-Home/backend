from flask import render_template, flash, redirect, request
from app import app, db
from app.view.forms import LoginForm
from app.model.Users import Users
from app.model.Offers import Offers
from app.model.Notifications import Notifications
from app.model.ParkingPlaces import ParkingPlaces
from app.model.Reservation import Reservation
import json


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
    return json.dumps(response)


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


@app.route('/home')
def index():
    user = {'nickname': 'Miguel'}  # выдуманный пользователь
    return render_template("index.html", user=user)

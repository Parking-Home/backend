# coding: utf-8
from flask import render_template, flash, redirect, request
from app import app
from app.control import controller
from app.view.forms import LoginForm


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


@app.route('/mailru-domainyB8u9f6URadENYFY.html')
def function():
    return render_template('mailru-domainyB8u9f6URadENYFY.html')


@app.route('/api/web', methods=['POST'])
def api_web():
    return controller.handle_request(request)


@app.route('/')
def hello_world():
    return redirect('/login')


@app.route('/home')
def index():
    user = {'nickname': 'Miguel'}
    return render_template("index.html", user=user)

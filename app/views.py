from flask import render_template, flash, redirect
from app import app
from app.view.forms import LoginForm


# функция представления index опущена для краткости

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


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # выдуманный пользователь
    return render_template("index.html", user=user)


@app.route('/posts')
def posts():
    user = {'nickname': 'Miguel'}  # выдуманный пользователь
    posts = [  # список выдуманных постов
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("posts.html",
                           title='Home',
                           user=user,
                           posts=posts)

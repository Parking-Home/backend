from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # выдуманный пользователь
    return render_template("index.html", title='Home', user=user)


if __name__ == '__main__':
    app.run()

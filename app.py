from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)


# dashboard series
@app.route('/dashboard')
def dashboard():
    return 'Hello World!'


@app.route('/getOccupy')
def getOccupy():
    return 'Hello World!'


# submit series
@app.route('/submit')
def submit():
    return 'Hello World!'


@app.route('/submitResult')
def submitResult():
    return 'Hello World!'


# record series
@app.route('/record')
def record():
    return 'Hello World!'


@app.route('/withdraw')
def withdraw():
    return 'Hello World!'


@app.route('/message')
def message():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

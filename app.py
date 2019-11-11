from flask import Flask,request

app = Flask(__name__)


@app.route('/dashboard')
def dashboard():
    return 'Hello World!'

@app.route('/submit')
def ():
    return 'Hello World!'

@app.route('/checkAvailable')
def checkAvailable():
    return 'Hello World!'

@app.route('/')
def ():
    return 'Hello World!'

@app.route('/')
def ():
    return 'Hello World!'

@app.route('/')
def ():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

from flask import Flask, request

app = Flask(__name__)


# dashboard series
# 教室占用网页
@app.route('/dashboard')
def dashboard():
    return 'Hello World!'


# 根据日期返回教室占用
@app.route('/getOccupy')
def getOccupy():
    return 'Hello World!'


# submit series
# 返回网页 （借哪个教室）
@app.route('/submit')
def submit():
    return 'Hello World!'


@app.route('/submitResult')
def submitResult():
    return 'Hello World!'


# record series
# 订单
@app.route('/record')
def record():
    return 'Hello World!'


# 撤回
@app.route('/withdraw')
def withdraw():
    return 'Hello World!'


@app.route('/')
def home():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

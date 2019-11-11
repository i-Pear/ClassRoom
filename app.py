from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json
import time

app = Flask(__name__)
db = SQLAlchemy(app)
# key：教室名称如 一号楼A302 类型string
# value：教室状态如 000000000000 类型int
room_occupy = {"2019/10/01": {"一号楼A302": 0}}


# dashboard series
# 教室占用网页
@app.route('/dashboard')
def dashboard():
    now = time.strftime("%Y-%m-%d", time.localtime())
    print(now)
    return 'Hello World!'


# 根据日期返回教室占用
@app.route('/getOccupy')
def getOccupy():
    date = str(request.args["date"])
    if date in room_occupy:
        return json.dumps(room_occupy[date])
    return json.dumps({})


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

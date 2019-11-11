from flask import Flask, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import init_db
import json

app = Flask(__name__)
db = SQLAlchemy(app)
# key：教室名称如 一号楼A302 类型string
# value：教室状态如 000000000000 类型int
room_occupy = {"2019/10/01": {"一号楼A302": 0}}


# dashboard series
# 教室占用网页
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


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
    return render_template("submit.html")


@app.route('/submitResult')
def submitResult():
    return 'Hello World!'


# record series
# 订单 渲染
@app.route('/record')
def record():
    return 'Hello World!'


# 撤回
@app.route('/withdraw')
def withdraw():
    withdrawID = str(request.args["id"])


@app.route('/')
def home():
    return redirect("/dashboard")


if __name__ == '__main__':
    app.run()

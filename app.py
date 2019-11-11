from flask import Flask, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import json
import time
import urllib.request

WECHAT_APPID = ""
WECHAT_APPSECRET = ""

app = Flask(__name__)
db = SQLAlchemy(app)
# key：教室名称如 一号楼A302 类型string
# value：教室状态如 000000000000 类型int
room_occupy = {"2019/10/01": {"一号楼A302": 0}}


def getOpenID(code):
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (
        WECHAT_APPID, WECHAT_APPSECRET, code)
    response = urllib.request.urlopen(url)
    resp_dict = json.loads(response.read())
    return resp_dict["openid"]


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
    openid = getOpenID(str(request.args["code"]))
    return render_template("submit.html")


@app.route('/submitResult')
def submitResult():
    return 'Hello World!'


# record series
# 订单 渲染
@app.route('/record')
def record():
    openid = getOpenID(str(request.args["code"]))
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

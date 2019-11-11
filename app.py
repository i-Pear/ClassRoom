from flask import Flask, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from entity import *
import json
import time
import urllib.request

WECHAT_APPID = ""
WECHAT_APPSECRET = ""

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
import init_db

# key：教室名称如 一号楼A302 类型string
# value：教室状态如 000000000000 类型int
room_occupy = {"2019/10/01": {"一号楼A302": 0}}


# Accepted √
def getOpenID(code):
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (
        WECHAT_APPID, WECHAT_APPSECRET, code)
    response = urllib.request.urlopen(url)
    resp_dict = json.loads(response.read())
    return resp_dict["openid"]


def getStuID(openid):
    # 在这里查询student数据库
    return "20184444"


# dashboard series
# 教室占用网页
# Accepted √
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
    jd = request.json
    date = jd["date"]
    # TODO 这里要对date做校验,至于怎样算是一个合法的日期输入呢？我们不得而知

    request_time = datetime.datetime.now()
    req = RequestEntry(int(jd["stuid"]), jd["classroom"], date, jd["segment"], str(request_time))
    db.session.add(req)
    db.session.commit()
    return 'OK!'


# record series
# 订单 渲染
@app.route('/record')
def record():
    openid = getOpenID(str(request.args["code"]))
    stuid = getStuID(openid)
    request_records = RequestEntry.query.filter(RequestEntry.stuid == stuid).all()
    # TODO 把过期的请求删一下

    return render_template("record.html", records=request_records)


# 撤回
@app.route('/withdraw')
def withdraw():
    withdrawID = str(request.args["id"])


# Accepted √
@app.route('/')
def home():
    return redirect("/dashboard")


# 绑定用户
@app.route('/bind')
def bind():
    return render_template("bind.html")


# 验证用户绑定信息
@app.route('/bindCheck')
def bindCheck():
    return "ok"

# Accepted √
if __name__ == '__main__':
    app.run()

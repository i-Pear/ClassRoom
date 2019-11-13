from flask import Flask, request, url_for, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os
import json
import time
import urllib.request
from args_format import *
from hashlib import sha1

WECHAT_APPID = ""
WECHAT_APPSECRET = ""

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365 // 2)
app.config.from_object('config')
db = SQLAlchemy(app)
import init_db
from entity import *

# key：教室名称如 一号楼_A302 类型string
# value：教室状态如 000000000000 类型int
room_occupy = {"20191001": {"一号楼_A302": 0}}


# Accepted √
def getOpenID(code):
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (
        WECHAT_APPID, WECHAT_APPSECRET, code)
    response = urllib.request.urlopen(url)
    resp_dict = json.loads(response.read())
    return resp_dict["openid"]


def getStuID(openid):
    # 在这里查询student数据库
    answers = StudentEntry.query.filter(openid=int(openid)).all()
    for ans in answers:
        return True, ans.stuid
    return False, -1


# dashboard series
# 教室占用网页
# Accepted √
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


# 根据日期返回教室占用
@app.route('/getOccupy', methods=['POST'])
def getOccupy():
    date = str(request.args["date"])
    if not is_allowed_date(date):
        return json.dumps({
            "state": -1,
            "message": "format error"
        })
    if date in room_occupy:
        return json.dumps({
            "state": 231,
            "message": "request success",
            "data": room_occupy[date]
        })
    return json.dumps({
        "state": 232,
        "message": "request success, no room occupied",
        "data": {}
    })


# 返回单个房间的占用情况
@app.route("/getOccupyByRoom", methods=['POST'])
def getOccupyByRoom():
    room = str(request.args["room"])
    date = str(request.args["date"])
    if not is_allowed_date(date) or not is_allowed_room(room):
        return json.dumps({
            "state": -1,
            "message": "format error"
        })
    answers = ClassroomEntry.query.filter(ClassroomEntry.classroom == room and ClassroomEntry.date == int(date)).all()
    for ans in answers:
        return json.dumps({
            "state": 231,
            "message": "get success",
            "data": ans.occupy
        })
    return json.dumps({
        "state": -1,
        "message": "can't find the room in this date"
    })


# submit series
# 返回网页 （借哪个教室）
@app.route('/submit')
def submit():
    return render_template("submit.html")


@app.route('/submitResult', methods=['POST'])
def submitResult():
    jd = request.json
    openid = session[session.get("user")]
    if openid is None:
        return json.dumps({
            "state": -1,
            "message": "access denied"
        })
    room = str(jd["room"])
    date = jd["date"]
    seg = int(jd["segment"])
    reason = str(jd["requestReason"])
    success, stuid = getStuID(openid)
    if not (success and is_allowed_room(room) and is_allowed_date(date) and is_allowed_reason(
            reason) and is_allowed_segment(seg)):
        return json.dumps({
            "state": -1,
            "message": "format error"
        })
    req = RequestEntry(stuid, room, date, seg, reason)
    db.session.add(req)
    db.session.commit()
    return json.dumps({
        "state": 233,
        "message": "submit success"
    })


# record series
# 订单
@app.route('/record')
def record():
    openid = session[session.get("user")]
    if openid is None:
        return json.dumps({
            "state": -1,
            "message": "access denied"
        })
    success, stuid = getStuID(openid)
    if not success:
        return json.dumps({
            "state": -1,
            "message": "invalid openid"
        })
    request_records = RequestEntry.query.filter(RequestEntry.stuid == stuid).all()
    recs = []
    for rec in request_records:
        if not is_expired(rec.date):
            recs.append({
                "id": rec.id,
                "stuid": rec.stuid,
                "classroom": rec.classroom,
                "date": rec.date,
                "segment": rec.segment,
                "requestTime": rec.requestTime,
                "requestReason": rec.requestReason,
                "status": rec.status
            })
    return json.dumps({
        "state": 233,
        "message": "records success",
        "date": recs
    })


# 撤回
@app.route('/withdraw')
def withdraw():
    openid = session[session.get("user")]
    if openid is None:
        return json.dumps({
            "state": -1,
            "message": "access denied"
        })
    success, stuid = getStuID(openid)
    if not success:
        return json.dumps({
            "state": -1,
            "message": "invalid openid"
        })
    withdrawID = str(request.args["id"])
    res = RequestEntry.query.filter(RequestEntry.stuid == stuid and RequestEntry.id == withdrawID).all()
    db.session.delete(res)
    db.session.commit()
    return json.dumps({
        "state": 233,
        "message": "delete success"
    })


# Accepted √
@app.route('/')
def home():
    return redirect(url_for(dashboard))


def get_student_from_db(stuid):
    anss = StudentEntry.query.filter(StudentEntry.stuid == stuid).all()
    for ans in anss:
        return ans
    return None


# 绑定用户
@app.route('/bind')
def bind():
    jd = request.json
    stuid = int(jd["stuid"])
    stu = get_student_from_db(stuid)
    sha1 = jd["authSha1"]
    if stu is None or stu.authSha1 != sha1:
        return json.dumps({
            "state": -1,
            "message": "invalid identity"
        })
    openid = getOpenID(jd["code"])
    stu.openid = openid
    db.session.commit()
    session.permanent = True
    session[session.get("user")] = openid
    return json.dumps({
        "state": 233,
        "message": "bind successful"
    })


# Accepted √
if __name__ == '__main__':
    app.run()

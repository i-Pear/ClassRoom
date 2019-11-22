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

__debug_mode__ = True

# key：教室名称如 一号楼_A302 类型string
# value：教室状态如 000000000000 类型int
room_occupy = {"20191001": {"一号楼_A302": 0, "建筑楼_A666": 0}}


def get_student_from_db(stuid):
    anss = StudentEntry.query.filter(StudentEntry.stuid == stuid).all()
    for ans in anss:
        and_f = StudentEntry(ans.stuid, ans.openid, ans.authSha1, ans.tempAuth)
        return and_f, ans
    return None


def getOpenID(code):
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (
        WECHAT_APPID, WECHAT_APPSECRET, code)
    response = urllib.request.urlopen(url)
    resp_dict = json.loads(response.read())
    return resp_dict["openid"]


def getStuID(openid):
    # 在这里查询student数据库
    answers = StudentEntry.query.filter(StudentEntry.openid == str(openid)).all()
    for ans in answers:
        return True, ans.stuid
    return False, -1


def add_occupy_to_date(date, room, seg):
    date = str(date)
    if date not in room_occupy:
        room_occupy[date] = {}
    if room not in room_occupy[date]:
        room_occupy[date][room] = 0
    if room_occupy[date][room] & seg != 0:
        return False
    if __debug_mode__:
        entry = ClassroomEntry.query.filter(ClassroomEntry.classroom == room).filter(
            ClassroomEntry.date == date).first()
        if entry is []:
            entry = ClassroomEntry(room, int(date), seg)
            db.session.add(entry)
            db.session.commit()
        else:
            entry.occupy |= seg
            db.session.commit()
    room_occupy[date][room] |= seg
    return True


# --------------- Pages ------------------

@app.route('/favicon.ico')
def icon():
    return redirect(url_for("static", filename="favicon.ico"))


# 主页面
@app.route('/')
def home():
    return redirect(url_for("static", filename="dashboard.html"))


# 教室占用网页
@app.route('/dashboard')
def dashboard():
    return redirect(url_for("static", filename="dashboard.html"))


# 返回网页 （借哪个教室）
@app.route('/submit')
def submit():
    return redirect(url_for("static", filename="submit.html"))


# 返回网页 （操作记录）
@app.route('/record')
def record():
    return redirect(url_for("static", filename="record.html"))


# 返回网页 （管理员界面）
@app.route('/admin')
def admin():
    return redirect(url_for("static", filename="admin.html"))


# @app.route('/static/<name>')
# def staticRes(name):
#     return redirect(url_for("static", filename=str(name)))


# --------------- Operations ------------------


# 根据日期返回教室占用
# POST参数：date
@app.route('/getOccupyOperation', methods=['POST'])
def getOccupyOperation():
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
# POST参数：room date
@app.route("/getOccupyByRoomOperation", methods=['POST'])
def getOccupyByRoomOperation():
    room = str(request.args["room"])
    date = str(request.args["date"])
    if not is_allowed_date(date) or not is_allowed_room(room):
        return json.dumps({
            "state": -1,
            "message": "format error"
        })
    answers = ClassroomEntry.query.filter(ClassroomEntry.classroom == room).filter(
        ClassroomEntry.date == int(date)).all()
    for ans in answers:
        return json.dumps({
            "state": 231,
            "message": "get success",
            "data": ans.occupy
        })
    return json.dumps({
        "state": 231,
        "message": "can't find the room in this date",
        "data": 0
    })


# 处理提交请求 并返回提交结果
# POST参数：room date segment requestReason
@app.route('/submitResultOperation', methods=['POST'])
def submitResultOperation():
    jd = request.json
    openid = session['username']
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
    sta = add_occupy_to_date(date, room, seg)
    if sta:
        return json.dumps({
            "state": 233,
            "message": "submit success"
        })
    else:
        return json.dumps({
            "state": -1,
            "message": "room conflict"
        })


# 返回订单
# POST参数：无
@app.route('/recordQueryOperation')
def recordQueryOperation():
    openid = session['username']
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
# POST 参数：id
@app.route('/withdrawOperation')
def withdrawOperation():
    openid = session['username']
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


# 绑定用户
# POST参数：stuid authSha1 code
@app.route('/bindOperation', methods=['POST'])
def bindOperation():
    jd = request.json
    stuid = int(jd["stuid"])
    stu, entry = get_student_from_db(stuid)
    sha1 = jd["authSha1"]
    if stu is None or stu.authSha1 != sha1:
        return json.dumps({
            "state": -1,
            "message": "invalid identity"
        })
    openid = None
    if __debug_mode__:
        openid = "123456"
    else:
        openid = getOpenID(jd["code"])
    entry.openid = openid
    db.session.commit()
    session.permanent = True
    session['username'] = openid
    return json.dumps({
        "state": 233,
        "message": "bind successful"
    })


if __name__ == '__main__':
    app.run()

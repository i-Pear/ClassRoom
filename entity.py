from app import db
import datetime


class RequestEntry(db.Model):
    __tablename__ = "requests"

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, autoincrement=1)
    stuid = db.Column(db.INTEGER, index=True, nullable=False)
    classroom = db.Column(db.VARCHAR(20), index=True, nullable=False)
    date = db.Column(db.INTEGER, nullable=False)
    segment = db.Column(db.INTEGER, index=True, nullable=False)
    requestTime = db.Column(db.DATETIME, nullable=False, default=datetime.datetime.now)
    requestReason = db.Column(db.VARCHAR(500), default="")
    status = db.Column(db.INTEGER, default=0)

    def __init__(self, stuid: int, classroom: str, date: int, segment: int, requestReason: str, ):
        self.stuid = stuid
        self.classroom = classroom
        self.date = date
        self.segment = segment
        self.requestReason = requestReason

    def __repr__(self):
        return f"<Entry of request {self.id}: stuid {self.stuid} requested classroom {self.classroom} on {self.date} segment {self.segment} " \
               f" requestTime:{self.requestTime} requestReason:{self.requestReason} status:{self.status}"


class ClassroomEntry(db.Model):
    __tablename__ = "classroom"

    classroom = db.Column(db.VARCHAR(20), index=True, nullable=False, primary_key=True)
    date = db.Column(db.INTEGER, index=True, nullable=False)
    occupy = db.Column(db.INTEGER, default=0)

    def __init__(self, classroom: str, date: int, occupy: int):
        self.classroom = classroom
        self.date = date
        self.occupy = occupy

    def __repr__(self):
        return f"<Entry of classroom: {self.classroom} @ {self.date} @ {self.occupy}"


class StudentEntry(db.Model):
    __tablename__ = "student"

    stuid = db.Column(db.INTEGER, primary_key=True, nullable=False)
    openid = db.Column(db.VARCHAR(64), index=True, nullable=False)
    authSha1 = db.Column(db.VARCHAR(64), default="")
    tempAuth = db.Column(db.VARCHAR(64), default="")

    def __init__(self, stuid: int, openid: str, authSha1: str, tempAuth: str):
        self.stuid = stuid
        self.openid = openid
        self.authSha1 = authSha1
        self.tempAuth = tempAuth

    def __repr__(self):
        return f"<Entry of student: {self.stuid} @ {self.openid} @ {self.authSha1} @ {self.tempAuth}"

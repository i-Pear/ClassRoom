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

    def __init__(self, id: int, stuid: int, classroom: str, date: int, segment: int, requestReason: str, ):
        self.id = id
        self.stuid = stuid
        self.classroom = classroom
        self.date = date
        self.segment = segment
        self.requestReason = requestReason

    def __repr__(self):
        return f"<Entry of request {self.id}: stuid {self.stuid} requested classroom {self.classroom} on {self.date} segment {self.segment} " \
               f" requestTime:{self.requestTime} requestReason:{self.requestReason} status:{self.status}"

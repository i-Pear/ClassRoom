from app import db

class Entry(db.Model):
    __tablename__ = "requests"

    id = db.Column(db.INTEGER, primary_key=True, nullable=False)
    stuid = db.Column(db.INTEGER, index=True, nullable=False)
    classroom = db.Column(db.VARCHAR(20), index=True, nullable=False)
    segment = db.Column(db.VARCHAR(32), index=True, nullable=False)
    requestTime = db.Column(db.DATE, unique=True, nullable=False)
    requestReason = db.Column(db.VARCHAR(500), nullable=True)
    choice = db.Column(db.VARCHAR(256), nullable=False)
    has_file = db.Column(db.BOOLEAN, nullable=False, default=False)

    def __init__(self, username: str, realname: str, academy: str,
                 clazz: str, phone: str, qq: str, choice: str, has_file: bool):
        self.username = username
        self.realname = realname
        self.academy = academy
        self.clazz = clazz
        self.phone = phone
        self.qq = qq
        self.choice = choice
        self.has_file = has_file

    def __repr__(self):
        return f"<Entry of user {self.username}: {self.realname} @ {self.clazz} of {self.academy} Tel {self.phone} " \
               f"Choice {self.choice} HasFile {self.has_file}>"


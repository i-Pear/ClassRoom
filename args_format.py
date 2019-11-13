import datetime

builds = []

with open(r'E:\Softs\Projects\pycharmProjects\ClassRoom\builds.txt', "r", encoding="utf-8") as f:
    build = f.readline()
    while build != "end_list" and build != "end_list\n":
        rooms = [build[:-1]]
        rooms += f.readline()[:-1].split(" ")
        builds.append(rooms)
        build = f.readline()


# 允许的日期为八位数字或字符串
def is_allowed_date(date):
    try:
        datetime.datetime.strptime(str(date), "%Y%m%d")
        return True
    except ValueError:
        return False


# 允许的房间名格式为 建筑楼_A301 建筑和房间按照一定格式写在builds.txt里面
def is_allowed_room(room):
    room = str(room)
    ros = room.split("_")
    if len(ros) != 2:
        return False
    for bul in builds:
        if bul[0] == ros[0] and ros[1] in bul[1:]:
            return True
    return False


# 允许的段为 0 - max_seg
def is_allowed_segment(segment, max_seg=12):
    if segment < 0 or segment >= max_seg:
        return False
    return True


# 允许的原因为 1 - max_reason
def is_allowed_reason(reason, max_reason = 500):
    reason = len(reason)
    if reason <= 1 or reason > max_reason:
        return False
    return True


# 判断日期是否过期,当天不算过期
def is_expired(date):
    date = str(date)
    dt = datetime.datetime.strptime(str(date), "%Y%m%d")
    now = datetime.datetime.now() + datetime.timedelta(days=1)
    if now < dt:
        return False
    return True

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


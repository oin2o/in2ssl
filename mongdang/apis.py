import datetime

from .models import User, Note


# 위도 기준 +0.01이 약 +1km, 경도 기준 +0.015가 약 +1km
latitude_range = 0.005
longitude_range = 0.0075


def getnotes(latitude, longitude):
    now = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')

    notes = Note.objects.filter(endtime__gt=now, latitude__range=(float(latitude)-latitude_range, float(latitude)+latitude_range), longitude__range=(float(longitude)-longitude_range, float(longitude)+longitude_range)).order_by('endtime')

    return notes


def addnote(username, contents, latitude, longitude):
    user = User.objects.filter(username=username).first()

    now = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')

    # 새로고침 등으로 동일 내용이 입력되는 경우는 추가하지 않음
    note = Note.objects.filter(user=user, endtime__gt=now, contents=contents)

    if not note:
        value, created = Note.objects.get_or_create(
            user=user,
            contents=contents,
            latitude=latitude,
            longitude=longitude,
            registtime=now,
            endtime=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(minutes=10), '%Y%m%d%H%M%S'),
        )

        return True
    else:
        return False

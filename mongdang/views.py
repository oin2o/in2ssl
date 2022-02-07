import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views import generic

from .models import User, Note


# 위도 기준 +0.01이 약 +1km, 경도 기준 +0.015가 약 +1km
latitude_range = 0.005
longitude_range = 0.0075


class MainView(generic.ListView):
    template_name = "mongdang/main.html"

    def get(self, request):
        user_only_guest = User.objects.filter(delYn=False, username__startswith='손님').order_by('username')
        user_exclude_guest = User.objects.filter(delYn=False).exclude(username__startswith='손님').order_by('username')

        user_list = list(user_only_guest) + list(user_exclude_guest)

        context = {
            'user_list': user_list,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get('action')
        username = request.POST.get('username')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # 사용자 명이 없는 경우, 에러로 메인화면으로 전송
        if len(username) == 0:
            return HttpResponseRedirect(reverse('mongdang:main', ))

        # 사용자 명으로 신규 생성하거나, 기존 사용자 조회
        user, created = User.objects.get_or_create(username=username)

        if action == "login":
            now = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')

            notes = Note.objects.filter(endtime__gt=now, latitude__range=(float(latitude)-latitude_range, float(latitude)+latitude_range), longitude__range=(float(longitude)-longitude_range, float(longitude)+longitude_range))

            context = {
                'user': user,
                'latitude': latitude,
                'longitude': longitude,
                'notes': notes,
            }

            return render(request, "mongdang/paper.html", context)

        return HttpResponseRedirect(reverse('mongdang:main', ))


class PaperView(generic.ListView):
    template_name = "mongdang/paper.html"

    def post(self, request, username):
        user = User.objects.filter(username=username).first()

        action = request.POST.get('action')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        contents = request.POST.get('contents')

        now = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')

        if action == "addnote":
            # 새로고침 등으로 동일 위치에서 동일 내용이 입력되는 경우는 추가하지 않음
            note = Note.objects.filter(user=user, endtime__gt=now, contents=contents, latitude=latitude, longitude=longitude)

            if not note:
                value, created = Note.objects.get_or_create(
                    user=user,
                    contents=contents,
                    latitude=latitude,
                    longitude=longitude,
                    registtime=now,
                    endtime=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(minutes=10), '%Y%m%d%H%M%S'),
                )

        elif action == "addcomment":
            print("댓글 등록")

        notes = Note.objects.filter(endtime__gt=now, latitude__range=(float(latitude)-latitude_range, float(latitude)+latitude_range), longitude__range=(float(longitude)-longitude_range, float(longitude)+longitude_range))

        context = {
            'user': user,
            'latitude': latitude,
            'longitude': longitude,
            'notes': notes,
        }

        return render(request, self.template_name, context)

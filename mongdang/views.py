from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views import generic

from .models import User

from .apis import getnotes, addnote


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
            notes = getnotes(latitude, longitude)

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

    def get(self, request, username):
        return HttpResponseRedirect(reverse('mongdang:main', ))

    def post(self, request, username):
        user = User.objects.filter(username=username).first()

        action = request.POST.get('action')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        contents = request.POST.get('contents')

        if action == "addnote":
            addnote(user.username, contents, latitude, longitude)

        elif action == "addcomment":
            print("댓글 등록")

        notes = getnotes(latitude, longitude)

        context = {
            'user': user,
            'latitude': latitude,
            'longitude': longitude,
            'notes': notes,
        }

        return render(request, self.template_name, context)

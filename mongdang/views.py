from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views import generic

from .models import User
from .apis import getnotes, addnote, getcomments, addcomment
from .serializers import NoteSerializer, CommentSerializer


class NotesAPI(APIView):
    @staticmethod
    def post(request):
        action = request.POST.get('action')
        username = request.POST.get('username')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if action == "getnotes":
            # 좌표값이 있는 경우, 근처의 쪽지 조회
            if latitude and longitude:
                notes = getnotes(latitude, longitude)
                serializer = NoteSerializer(notes, many=True)
                return Response(serializer.data)

        return Response("")


class CommentsAPI(APIView):
    @staticmethod
    def post(request):
        action = request.POST.get('action')
        username = request.POST.get('username')
        noteid = request.POST.get('noteid')
        comment = request.POST.get('comment')

        if action == "getcomments":
            # 노트 ID가 있는 경우, 해당 노트의 댓글 조회
            if noteid:
                comments = getcomments(noteid)
                serializer = CommentSerializer(comments, many=True)
                return Response(serializer.data)

        elif action == "addcomment":
            print(noteid, username, comment)
            # 노트 ID, 사용자, 댓글이 모두 있는 경우만 등록
            if noteid and username and comment:
                result = addcomment(username, noteid, comment)
                if result:
                    comments = getcomments(noteid)
                    serializer = CommentSerializer(comments, many=True)
                    return Response(serializer.data)

        return Response("")


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

    @staticmethod
    def post(request):
        action = request.POST.get('action')
        username = request.POST.get('username')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # 사용자, 좌표 등이 없는 경우, 에러로 메인화면으로 전송
        if not username or not latitude or not longitude:
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

        # 입력 데이터가 정상적인 경우만, 노트 및 댓글 등록
        if username and latitude and longitude and contents:
            if action == "addnote":
                addnote(user.username, contents, latitude, longitude)

        notes = getnotes(latitude, longitude)

        context = {
            'user': user,
            'latitude': latitude,
            'longitude': longitude,
            'notes': notes,
        }

        return render(request, self.template_name, context)

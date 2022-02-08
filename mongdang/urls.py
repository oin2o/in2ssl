from django.urls import path
from . import views

app_name = 'mongdang'

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('<str:username>', views.PaperView.as_view(), name='paper'),
    path('api/notes/', views.NotesAPI.as_view()),
    path('api/comments/', views.CommentsAPI.as_view()),
]

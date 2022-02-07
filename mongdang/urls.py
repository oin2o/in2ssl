from django.urls import path
from . import views

app_name = 'mongdang'

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('<str:username>', views.PaperView.as_view(), name='paper'),
]

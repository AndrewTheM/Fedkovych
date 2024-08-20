from django.urls import path
from . import views

urlpatterns = [
    path('', views.stream_player, name='stream_player'),
]
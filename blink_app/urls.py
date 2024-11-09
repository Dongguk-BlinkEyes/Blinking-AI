from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 기본 페이지
    path('video_feed/', views.video_feed, name='video_feed'),  # 비디오 피드 URL
]

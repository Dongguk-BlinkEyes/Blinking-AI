"""
URL configuration for Blinking_AI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blink_app import views  # blink_app은 사용자의 앱 이름입니다.

urlpatterns = [
    path("admin/", admin.site.urls),
    path("video_feed/", views.video_feed, name="video_feed"),  # 비디오 스트림 경로
    path("", views.index, name="index"),  # 기본 페이지 경로
]

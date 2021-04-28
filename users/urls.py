from django.urls import path

from .views import KakaoLogin

urlpatterns = [
    path('/login/kakao', KakaoLogin.as_view()),
]

# from django.urls import path
# from .views import * # user>views에서 모든 함수를 가져온다.
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = "common"
urlpatterns = [
  path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), # 수정해야하는 코드
  # django.contrib.auth앱의 LoginView 클래스를 활용했으므로 별도의 views.py 파일 수정이 필요 없음
  path('logout/', auth_views.LogoutView.as_view(), name='logout'), # 코드 추가하기
]
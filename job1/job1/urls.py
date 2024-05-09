"""
URL configuration for job1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from jobs import views

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url
from django.views.static import serve

urlpatterns = [
    path('jobs/', include('jobs.urls')), #jobs로 시작하는 모든 url은 jobs>urls.py 파일을 참조할 것이다. 즉 jobs부터 치고 다음 주소를 쳐야 한다.
    #path("users/", include('users.urls')), #users으로 시작하는 모든 url은 모두 users>urls.py 파일을 참조할 것이다.
    path("admin/", admin.site.urls), #admin치고 들어가면 됨
    path('job2/', include('job2.urls')), #job2로 시작하는 모든 url은 job2>urls.py 파일을 참조할 것이다. 즉 job2부터 치고 다음 주소를 쳐야 한다.
    # path('common/', include('common.urls')), #common으로 시작하는 모든 url은 common/urls.py 파일을 참조할 것이다.
    path('', include('common.urls'))
]

# 배포시 추가
urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
"""
Django settings for job1 project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-s0=g(aab+0xz#*s^v+cwukx=9$=^1=8=z(ntr^a!rm)19_isk!"

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True ##배포할때는 false로
DEBUG = False #배포때 추가

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*'] # 모든 호스트 허용. 배포때 추가

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "jobs", #job1 프로젝트의 jobs 웹앱 추가
    "job2",
    "common.apps.CommonConfig", #로그인용 웹앱 추가. 이름은 common으로 지었다. 
    # "js_lib_ag_grid_community", #django aggrid app
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "job1.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "job1.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # mysqlclient library 설치 필요
        'NAME': 'betadb', #MariaDB에서 내가 접근할 DB이름 testdb / betadb / jobdb(운영)
        'USER': 'cdh', #내 계정(모든 권한이 필요함)
        'PASSWORD': 'cdh0706**', #내 계정의 비밀번호 - 개발서버: cdh0706** / 운영서버: 1234
        'HOST': '130.1.112.100', #DB IP주소 - 개발서버 IP: 130.1.112.100 / 운영서버 IP: 130.1.200.200
        'PORT': '3306' #DB port
    }

#    여기 작성한 다음에 migration해주면 바로 연동됨. 그 후에 shell 이용해서 데이터 확인해보기.
#    "default": {
#        "ENGINE": "django.db.backends.sqlite3",
#        "NAME": BASE_DIR / "db.sqlite3",
#    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC" #UTC

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# 원본 - job1(프로젝트 폴더)의 settings.py였다.
# STATIC_URL = "static/"

# jobs 웹앱 폴더 밑에 static을 관리했다. 이거를 프로젝트 폴더에서 관리할 것이다.
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "jobs/static"),
# ]

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    # BASE_DIR / 'job1/static', 배포전
    os.path.join(BASE_DIR, 'job1', 'static'), # 배포후
    os.path.join(BASE_DIR, 'common', 'static'), # 배포후
]

# 배포때 추가된 코드
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  #이렇게 하면 collectstatic 명령어로 static 파일을 한 곳에 모아준다. 

# 미디어(배포때 추가)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 로그인 성공 시 자동으로 이동할 URL
LOGIN_REDIRECT_URL = '/jobs/main'

# 로그아웃 성공 시 자동으로 이동할 URL
# LOGOUT_REDIRECT_URL = '/common/login'
LOGOUT_REDIRECT_URL = '/'

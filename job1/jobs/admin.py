from django.contrib import admin
from .models import BsPrd #BsPrd 모델을 import
#from .models import TextConfirm

# Register your models here.
admin.site.register(BsPrd) #admin 사이트에 BsPrd 모델을 등록함 - 볼 수 있음
#admin.site.register(TextConfirm)
from django.urls import path
from django.shortcuts import render #template 호출. 즉, loader()와 HttpResponse()를 합친 개념
from . import views

urlpatterns = [
    path('table_test/', views.table_test, name='table_test'),
    path('test2/', views.test2, name='test2'),
    path('test3/', views.test3, name='test3'),
    path('test4/', views.test4, name='test4'),
    path('test5/', views.test5, name='test5'),
    path('test6/', views.test6, name='test6'),
    path('table/', views.table, name='table'),
    path('my_view/', views.my_view, name='my_view'),
    path('my_view_2/', views.my_view_2, name='my_view_2'),
    path('submit_data/', views.submit_data, name='submit_data'),
    
]
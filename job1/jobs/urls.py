from django.urls import path
from django.shortcuts import render #template 호출. 즉, loader()와 HttpResponse()를 합친 개념
from . import views

# 배포 때 추가
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url
from django.views.static import serve


urlpatterns = [
    path('', views.index, name='index'),
    # path('ag_grid/', views.ag_grid, name='ag_grid'),
    # path('ag_grid_pr/', views.ag_grid_pr, name='ag_grid_pr'),
    # path('ag_grid_pr_1/', views.ag_grid_pr_1, name='ag_grid_pr_1'),
    # path('ag_grid_pr_2/', views.ag_grid_pr_2, name='ag_grid_pr_2'),
    path('AGgrid/', views.my_view, name='AGgrid'),
    path('BS101/', views.BS101, name='BS101'), #회기 복사
    path('BS200/', views.BS200, name='BS200'), #회기 시작일 종료일 등록
    path('BS300/', views.BS300, name='BS300'),
    # path('BS301/', views.BS301, name='BS301'),
    # path('BS302/', views.BS302, name='BS302'),
    # path('BS303/', views.BS303, name='BS303'),
    path('BS103/', views.BS103, name='BS103'), #회기 확정
    # path('BS104/', views.BS104, name='BS104'), #회기 삭제
    path('BS105/', views.BS105, name='BS105'), #회기 표준 정보
    path('BS106/', views.BS106, name='BS106'), #회기별 공통 직무
    # path('BS104_pr/', views.BS104_pr, name='BS104_pr'), #회기 삭제
    # path('CC101_1/', views.CC101_1, name='CC101_1'),
    # path('CC102_1/', views.CC102_1, name='CC102_1'),
    path('CC102/', views.CC102, name='CC102'),
    path('CC105/', views.CC105, name='CC105'),
    path('JB101/', views.JB101, name='JB101'),
    path('JB102/', views.JB102, name='JB102'),
    # path('JB102_copy/', views.JB102_copy, name='JB102_copy'),
    path('JB103/', views.JB103, name='JB103'),
    # path('JB104/', views.JB104, name='JB104'),
    path('JB103_1/', views.JB103_1, name='JB103_1'),
    path('JB103_2/', views.JB103_2, name='JB103_2'),
    path('JB103_3/', views.JB103_3, name='JB103_3'),
    path('JB103_4/', views.JB103_4, name='JB103_4'),
    # path('JB103_test4/', views.JB103_test4, name='JB103_test4'),
    # path('JB103_test4_1/', views.JB103_test4_1, name='JB103_test4_1'),
    path('JB103_grid/', views.JB103_grid, name='JB103_grid'),
    path('JB108/', views.JB108, name='JB108'),
    path('JB109/', views.JB109, name='JB109'),
    path('JB110/', views.JB110, name='JB110'),
    path('JB200/', views.JB200, name='JB200'),
    path('JB300/', views.JB300, name='JB300'),
    path('create_bs_prd/', views.create_bs_prd, name='create_bs_prd'),
    path('BS200_2', views.BS200_2, name='BS200_2'),
    path('BS103_1/', views.BS103_1, name='BS103_1'),
    path('BS103_2/', views.BS103_2, name='BS103_2'),
    # path('delete_bs_prd/', views.delete_bs_prd, name='delete_bs_prd'),
    # path('change/', views.change, name='change'),
    # path('CC102_1_1/', views.CC102_1_1, name='CC102_1_1'),
    path('CC102_a/', views.CC102_a, name='CC102_a'),
    path('CC102_b/', views.CC102_b, name='CC102_b'),
    path('CC102_c/', views.CC102_c, name='CC102_c'),
    # path('BS104_pr_1/', views.BS104_pr_1, name='BS104_pr_1'),
    # path('delete_bs_prd_pr/', views.delete_bs_prd_pr, name='delete_bs_prd_pr'),
    # path('delete_bs_code_detail/', views.delete_bs_code_detail, name='delete_bs_code_detail'),
    # path('new_bs_code_detail/', views.new_bs_code_detail, name='new_bs_code_detail'),
    # path('create_bs_code_detail/', views.create_bs_code_detail, name='create_bs_code_detail'),
    path('BS105_1/', views.BS105_1, name='BS105_1'),
    path('BS105_2/', views.BS105_2, name='BS105_2'),
    path('BS106_1/', views.BS106_1, name='BS106_1'),
    path('BS106_2/', views.BS106_2, name='BS106_2'),
    path('BS106_3/', views.BS106_3, name='BS106_3'),
    path('BS106_4/', views.BS106_4, name='BS106_4'),
    path('BS200_1/', views.BS200_1, name='BS200_1'),
    path('BS300_1/', views.BS300_1, name='BS300_1'),
    path('BS300_2/', views.BS300_2, name='BS300_2'),
    path('BS300_3/', views.BS300_3, name='BS300_3'),
    path('BS300_4/', views.BS300_4, name='BS300_4'),
    path('BS300_5/', views.BS300_5, name='BS300_5'),
    path('BS300_6/', views.BS300_6, name='BS300_6'),
    # path('BS301_1/', views.BS301_1, name='BS301_1'),
    # path('BS301_2/', views.BS301_2, name='BS301_2'),
    # path('BS302_1/', views.BS302_1, name='BS302_1'),
    # path('BS303_1/', views.BS303_1, name='BS303_1'),
    # path('BS303_2/', views.BS303_2, name='BS303_2'),
    path('jb101_1/', views.jb101_1, name='jb101_1'),
    path('jb101_2/', views.jb101_2, name='jb101_2'),
    path('jb101_3/', views.jb101_3, name='jb101_3'),
    path('jb101_4/', views.jb101_4, name='jb101_4'),
    path('JB102_1/', views.JB102_1, name='JB102_1'),
    path('JB102_2/', views.JB102_2, name='JB102_2'),
    path('JB102_3/', views.JB102_3, name='JB102_3'),
    path('JB102_4/', views.JB102_4, name='JB102_4'),
    path('JB102_5/', views.JB102_5, name='JB102_5'),
    # path('JB102_copy_1/', views.JB102_copy_1, name='JB102_copy_1'),
    # path('JB102_copy_2/', views.JB102_copy_2, name='JB102_copy_2'),
    # path('JB102_copy_3/', views.JB102_copy_3, name='JB102_copy_3'),
    # path('JB102_copy_4/', views.JB102_copy_4, name='JB102_copy_4'),
    # path('JB102_copy_5/', views.JB102_copy_5, name='JB102_copy_5'),
    # path('JB102_copy_6/', views.JB102_copy_6, name='JB102_copy_6'),
    # path('jb_103_0/', views.jb103_0, name='jb103_0'),   
    # path('jb_103_1/', views.jb103_1, name='jb103_1'),
    # path('jb_103_2/', views.jb103_2, name='jb103_2'),
    # path('jb_103_3/', views.jb103_3, name='jb103_3'),
    #path('jb_103_4/', views.jb103_4, name='jb103_4'),
    # path('jb103_test_0/', views.jb103_test_0, name='jb103_test_0'),
    # path('jb103_test_1/', views.jb103_test_1, name='jb103_test_1'),
    # path('jb103_test2_job/', views.jb103_test2_job, name='jb103_test2_job'),
    # path('jb103_test2_duty/', views.jb103_test2_duty, name='jb103_test2_duty'),
    # path('jb103_test2_task/', views.jb103_test2_task, name='jb103_test2_task'),
    # path('jb103_test2_activity/', views.jb103_test2_activity, name='jb103_test2_activity'),
    path('JB103_grid_1/', views.JB103_grid_1, name='JB103_grid_1'),
    path('JB103_grid_2/', views.JB103_grid_2, name='JB103_grid_2'),
    path('JB108_1/', views.JB108_1, name='JB108_1'),
    path('JB108_2/', views.JB108_2, name='JB108_2'),
    path('JB108_3/', views.JB108_3, name='JB108_3'),
    path('JB109_1/', views.JB109_1, name='JB109_1'),
    path('JB109_2/', views.JB109_2, name='JB109_2'),
    path('JB109_3/', views.JB109_3, name='JB109_3'),
    path('JB109_4/', views.JB109_4, name='JB109_4'),
    path('JB110_1/', views.JB110_1, name='JB110_1'),
    path('JB110_2/', views.JB110_2, name='JB110_2'),
    path('JB200_1/', views.JB200_1, name='JB200_1'),
    path('JB200_2/', views.JB200_2, name='JB200_2'),
    path('JB300_1/', views.JB300_1, name='JB300_1'),
    path('popup/', views.popup, name='popup'),
    path('', views.home, name='home'),
    path('test/', views.test, name='test'),
    path('main/', views.main, name='main'),
    # path('get_duty_names/', views.get_duty_names, name='get_duty_names'),
    # path('get_tasks/', views.get_tasks, name='get_tasks'),
    # path('get_activities/', views.get_activities, name='get_activities'),
    # path('submit_activity/', views.submit_activity, name='submit_activity'),
]

# 배포 때 추가
urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
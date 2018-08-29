from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import url

from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage


from . import views

from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView


from . import views

urlpatterns = [
    url(r'search_form.html', TemplateView.as_view(template_name='testapp/search_form.html'), name="home"),
    path('gene/', views.search_form, name='search_form'),
    url('w3school/', views.w3school_form, name='w3school'),
    path('search/', views.simple_upload, name='simple_upload'),
    path('graph1/', views.graph1, name='graph1'),
    path('graph2/', views.graph2, name='graph2'),
    path('graph3/', views.graph3, name='graph3'),
    path('graph4/', views.graph4, name='graph4'),
    path('graph5/', views.graph5, name='graph5'),
    path('graph6/', views.graph6, name='graph6'),
    path('chart/data/', views.ChartData.as_view()),
    path('mobile/data/', views.MobileData.as_view()),
    path('mobile/data1/', views.MobileData1.as_view()),
    path('mobile/data2/', views.MobileData2.as_view()),
    path('mobile/data3/', views.MobileData3.as_view()),
    path('mobile/data4/', views.MobileData4.as_view()),
    path('mobile/data5/', views.MobileData5.as_view()),
    url(r'^api/data/$', views.get_data, name='api-data'),
    url(r'^$', views.w3school_form, name='w3school'),
      ]

urlpatterns += staticfiles_urlpatterns()





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
    url(r'home.html', TemplateView.as_view(template_name='testapp/home.html'), name="home"),
   # url(r'auroragraph5.html', TemplateView.as_view(template_name='testapp/auroragraph5.html'), name="auroragraph5"),
    url(r'aurora.html', TemplateView.as_view(template_name='testapp/aurora.html'), name="aurora"),
    url(r'aurorainput.html', TemplateView.as_view(template_name='testapp/aurorainput.html'), name="aurorainput"),
    path('gene/', views.search_form, name='search_form'),
    url('home/$', views.home, name='home'),
    path('search/', views.simple_upload, name='simple_upload'),
    path('aurora_input/', views.aurora_input, name='aurora_input'),
    path('aurorainput/', views.aurora_input, name='aurorainput'),
    path('graph1/', views.graph1, name='graph1'),
    path('graph2/', views.graph2, name='graph2'),
    path('graph3/', views.graph3, name='graph3'),
    path('graph4/', views.graph4, name='graph4'),
    path('graph5/', views.graph5, name='graph5'),
    path('graph6/', views.graph6, name='graph6'),
    path('graph7/', views.graph7, name='graph5'),
    path('graph8/', views.graph8, name='graph6'),
    path('chart/data/', views.ChartData.as_view()),
    path('mobile/data/', views.MobileData.as_view()),
    path('mobile/data1/', views.MobileData1.as_view()),
    path('mobile/data2/', views.MobileData2.as_view()),
    path('mobile/data3/', views.MobileData3.as_view()),
    path('mobile/data4/', views.MobileData4.as_view()),
    path('mobile/data5/', views.MobileData5.as_view()),
    path('mobile/data6/', views.MobileData6.as_view()),
    path('mobile/data7/', views.MobileData7.as_view()),

    path('aurora/data1/', views.auroradata1.as_view()),
    path('aurora/data2/', views.auroradata2.as_view()),
    path('aurora/data3/', views.auroradata3.as_view()),
    path('aurora/data4/', views.auroradata4.as_view()),
    path('aurora/data6/', views.auroradata6.as_view()),
    path('aurora/data7/', views.auroradata7.as_view()),

    path('auroragraph1/', views.auroragraph1, name='auroragraph1'),
    path('auroragraph2/', views.auroragraph2, name='auroragraph2'),
    path('auroragraph3/', views.auroragraph3, name='auroragraph3'),
    path('auroragraph4/', views.auroragraph4, name='auroragraph4'),
    path('auroragraph5/', views.disttribution, name='auroragraph5'),
    path('auroragraph6/', views.auroragraph6, name='auroragraph5'),
    path('auroragraph7/', views.auroragraph7, name='auroragraph5'),
    path('alertlogupload/', views.alertlogupload, name='alertlogupload'),
    path('alertloganalysis/', views.alertloganalysis, name='alertloganalysis'),

    url(r'^api/data/$', views.get_data, name='api-data'),
    url(r'^$', views.home, name='home'),

    url('selection/$', views.countries_view, name='select'),

      ]

urlpatterns += staticfiles_urlpatterns()





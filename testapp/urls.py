from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import url

from . import views

from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from . import views

urlpatterns = [
    path('gene/', views.search_form, name='search_form'),
    path('search/', views.search, name='search'),
    path('chart/data/', views.ChartData.as_view()),
    url(r'^api/data/$', views.get_data, name='api-data'),
    url(r'^$', views.HomeView.as_view(), name='home'),
]

urlpatterns += staticfiles_urlpatterns()





from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import url

from . import views

from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView


from . import views

urlpatterns = [
    url(r'search_form.html', TemplateView.as_view(template_name='testapp/search_form.html'), name="home"),
    path('gene/', views.search_form, name='search_form'),
    url('w3school/', views.w3school_form, name='w3school'),
    path('search/', views.search, name='search'),
    path('chart/data/', views.ChartData.as_view()),
    path('mobile/data/', views.MobileData.as_view()),
    url(r'^api/data/$', views.get_data, name='api-data'),
    url(r'^$', views.HomeView.as_view(), name='home'),
]

urlpatterns += staticfiles_urlpatterns()





from django.urls import path
from django.views.generic import TemplateView

from . import views

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gene/', views.search_form, name='search_form'),
    path('search/', views.search, name='search'),
]



from django.conf.urls import url
from .api import ListAPI,cardAPI
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^list$',ListAPI.as_view()),
    url(r'^card$',ListAPI.as_view()),
    url(r'^home$', TemplateView.as_view(template_name="djangular/home.html"))
]
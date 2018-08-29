from django.urls import path
from django.views.generic import TemplateView

from . import views

from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'form/',views.form),
    url(r'upload/',views.upload),

]


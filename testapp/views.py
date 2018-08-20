from django.template.loader import get_template
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import RequestContext
from django.template import loader
from django.http import Http404
from .fileoperations import fileop
from .MGMautomatio import final
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.views.generic import View




import json

# Create your views here.


def search_form(request):
    return render(request, 'testapp/search_form.html')

def search(request):
    if 'x' in request.GET:
        #message = 'You searched for: %r' % request.GET['x'] + request.GET['y']
        a=request.GET['x']
        b=request.GET['y']
        print(a)
        print(b)
        if (a==b):
            message="both strings are same"
            message1="test message"
            #list=fileop(a,b)
            #print(list)
            logs1 = {'name': "Genesis",
                     "age": 47,
                     }
        else:
            list = final(a, b)
            message = 'not matchin'

            logs1 = {"name":[list],}


    #return HttpResponse(logs)
    # return render_to_response("testapp/search_form1.html", {'logs1': logs1})
    return JsonResponse(logs1)


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs_count = User.objects.all().count()
        labels = ["Users", "Blue", "Yellow", "Green", "Purple", "Orange"]
        default_items = [qs_count, 23, 23, 3, 12, 2]
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)

def get_data(request, *args, **kwargs):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data) # http response


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'testapp/index.html', {"customers": 10})



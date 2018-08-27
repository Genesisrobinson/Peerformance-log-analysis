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
from .MGMtestautomation import generateTestSummary
from .MobileLogprocessing import summaryview
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.views.generic import View
from django.http import HttpResponseRedirect
from .MobileLogprocessing import summaryview




import json

# Create your views here.


def search_form(request):
    return render(request, 'testapp/search_form.html')

def w3school_form(request):
    return render(request, 'testapp/w3school.html')

def search(request):
    if 'x' in request.GET:
        #message = 'You searched for: %r' % request.GET['x'] + request.GET['y']
        a=request.GET['x']
        print(a)
        pivot=summaryview(a)

        returnmessage = str(a) + str(" ") + "is successfully processed"
        data = {
           "response": returnmessage,
        }
    return render_to_response("testapp/search_form1.html", {'data':data})



class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs_count = User.objects.all().count()
        labels = ["Users", "Blue", "Yellow", "Green", "Purple", "Orange","Users1", "Blue", "Yellow", "Green", "Purple", "Orange"]
        default_items = [qs_count, 23, 23, 3, 12, 2,23, 23, 3, 12, 2.34]
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)

class MobileData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs_count = User.objects.all().count()
        pivot = summaryview()
        labels = pivot["endpoint"]
        default_items=pivot["time"]
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



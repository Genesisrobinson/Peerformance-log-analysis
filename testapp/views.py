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
from .MobileLogsProcessor import processMobileLogs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.views.generic import View
from django.http import HttpResponseRedirect
from .models import endpointavgtime,endpointavgtime1,endpointavgtime2,endpointavgtime3,endpointavgtime4,endpointavgtime5,endpointavgtime6,endpointavgtime7
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from django.shortcuts import render
import openpyxl
from django.core.files.storage import FileSystemStorage
import os
import time
import json

# Create your views here.


def search_form(request):
    return render(request, 'testapp/search_form.html')

def home(request):
    return render(request, 'testapp/home.html')

def search(request):

    if 'x' in request.GET:
        #message = 'You searched for: %r' % request.GET['x'] + request.GET['y']
        a=request.GET['x']
        print(a)

        [df1, df2, df3, df4, df5, df6, df7, df8] = processMobileLogs(a)
        #delete existing objects from the model
        deleteobjects=endpointavgtime.objects.all()
        deleteobjects.delete()
        for x in df1.itertuples():
            x=endpointavgtime.objects.create(endpoint=x.endpoint,time=x.averageResponseTime)
            x.save()
        returnmessage = str(a) + str(" ") + "is successfully processed"
        data = {
           "response": returnmessage,
        }
    return render_to_response("testapp/search_form1.html", {'data':data})

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print("File name" + filename)
        print("file URL" + uploaded_file_url )
        Filelocation="D:/webapp/mysite/media/" + str(filename)
        print("fileLocation" + Filelocation)
        while not os.path.exists(Filelocation):
            time.sleep(1)
        [df1, df2, df3, df4, df5, df6, df7, df8] = processMobileLogs(Filelocation)
        #delete existing objects from the model
        deleteobjects = endpointavgtime.objects.all()
        deleteobjects.delete()
        for x in df1.itertuples():
            x = endpointavgtime.objects.create(endpoint=x.endpoint, time=x.averageResponseTime)
            x.save()

        deleteobjects = endpointavgtime1.objects.all()
        deleteobjects.delete()
        for x in df2.itertuples():
            x = endpointavgtime1.objects.create(endpoint=x.endpoint, time=x.averageResponseTime)
            x.save()

        deleteobjects = endpointavgtime2.objects.all()
        deleteobjects.delete()
        for x in df3.itertuples():
            x = endpointavgtime2.objects.create(endpoint=x.endpoint, time=x.averageResponseTime)
            x.save()

        deleteobjects = endpointavgtime3.objects.all()
        deleteobjects.delete()
        for x in df4.itertuples():
            x = endpointavgtime3.objects.create(endpoint=x.endpoint, time=x.averageResponseTime)
            x.save()

        deleteobjects = endpointavgtime4.objects.all()
        deleteobjects.delete()
        for x in df5.itertuples():
            x = endpointavgtime4.objects.create(endpoint=x.endpoint, time=x.averageResponseTime)
            x.save()

        deleteobjects = endpointavgtime5.objects.all()
        deleteobjects.delete()
        for x in df6.itertuples():
            x = endpointavgtime5.objects.create(endpoint=x.level, time=x.transactionCount)
            x.save()

        deleteobjects = endpointavgtime6.objects.all()
        deleteobjects.delete()
        for x in df7.itertuples():
            x = endpointavgtime6.objects.create(endpoint=x.endpoint, time=x.transactionCount)
            x.save()

        deleteobjects = endpointavgtime7.objects.all()
        deleteobjects.delete()
        for x in df8.itertuples():
            x = endpointavgtime7    .objects.create(endpoint=x.endpoint, time=x.transactionCount)
            x.save()

        return render(request, 'testapp/search_form.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'testapp/search_form.html')

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
        endpoint = endpointavgtime.objects.values_list("endpoint", flat=True)
        time = endpointavgtime.objects.values_list("time", flat=True)
        data = {
                "labels": endpoint,
                "default": time,
        }
        return Response(data)

class MobileData1(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs_count = User.objects.all().count()
        endpoint = endpointavgtime1.objects.values_list("endpoint", flat=True)
        time = endpointavgtime1.objects.values_list("time", flat=True)
        data = {
                "labels": endpoint,
                "default": time,
        }
        return Response(data)
class MobileData2(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs_count = User.objects.all().count()
        endpoint = endpointavgtime2.objects.values_list("endpoint", flat=True)
        time = endpointavgtime2.objects.values_list("time", flat=True)
        data = {
                "labels": endpoint,
                "default": time,
        }
        return Response(data)
class MobileData3(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs_count = User.objects.all().count()
        endpoint = endpointavgtime3.objects.values_list("endpoint", flat=True)
        time = endpointavgtime3.objects.values_list("time", flat=True)
        data = {
                "labels": endpoint,
                "default": time,
        }
        return Response(data)
class MobileData4(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs_count = User.objects.all().count()
        endpoint = endpointavgtime4.objects.values_list("endpoint", flat=True)
        time = endpointavgtime4.objects.values_list("time", flat=True)
        data = {
                "labels": endpoint,
                "default": time,
        }
        return Response(data)
class MobileData5(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs_count = User.objects.all().count()
        endpoint = endpointavgtime5.objects.values_list("endpoint", flat=True)
        time = endpointavgtime5.objects.values_list("time", flat=True)
        data = {
                "labels": endpoint,
                "default": time,
        }
        return Response(data)

class MobileData6(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs_count = User.objects.all().count()
        endpoint = endpointavgtime6.objects.values_list("endpoint", flat=True)
        time = endpointavgtime6.objects.values_list("time", flat=True)
        data = {
                "labels": endpoint,
                "default": time,
        }
        return Response(data)

class MobileData7(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs_count = User.objects.all().count()
        endpoint = endpointavgtime7.objects.values_list("endpoint", flat=True)
        time = endpointavgtime7.objects.values_list("time", flat=True)
        data = {
                "labels": endpoint,
                "default": time,
        }
        return Response(data)

def get_data(request, *args, **kwargs):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data) # http response


def graph1(request):
    return render(request, 'testapp/graph1.html')

def graph2(request):
    return render(request, 'testapp/graph2.html')

def graph3(request):
    return render(request, 'testapp/graph3.html')

def graph4(request):
    return render(request, 'testapp/graph4.html')

def graph5(request):
    return render(request, 'testapp/graph5.html')

def graph6(request):
    return render(request, 'testapp/graph6.html')

def graph7(request):
    return render(request, 'testapp/graph7.html')

def graph8(request):
    return render(request, 'testapp/graph8.html')
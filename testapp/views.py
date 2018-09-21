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
from .models import auroraaggregate,auroraice,auroratps,auroraaris,auroramlife,auroradmp,auroradistribution,aurorasummary,auroraerrorsummary,auroramethodsummary,auroraerrormethodsummary
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from django.shortcuts import render
import openpyxl
from django.core.files.storage import FileSystemStorage
import os
import time
import json
from  .AuroraPerfAnalytics import generateExcelCharts
import sqlite3
from mysite.settings import BASE_DIR
import django_tables2 as tables
from django_tables2 import RequestConfig
from .forms import CountryForm,VizInfoForm
from .models import EnrollmentApplication
from .AuroraAlertLogsProcessing import generateSummary
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

def aurora_input(request):
    if 'x' and 'y' and 'z' in request.GET:
        #message = 'You searched for: %r' % request.GET['x'] + request.GET['y']
        a=request.GET['x']
        b=request.GET['y']
        c=request.GET['z']
        print(a)
        filename = "report.xlsx"
        fs = FileSystemStorage()
        uploaded_file_url = fs.url(filename)

        engine = sqlite3.connect(str(BASE_DIR) + "/" + 'db.sqlite3')
        [df_agg, df_dmp, df_ice, df_mlife, df_tps, df_aris, df_dist] = generateExcelCharts(str(BASE_DIR) + "/media/report.xlsx", a, b, c)


        df_agg.to_sql('testapp_auroraaggregate', con=engine, if_exists='replace')
        df_dmp.to_sql('testapp_auroradmp', con=engine, if_exists='replace')
        df_ice.to_sql('testapp_auroraice', con=engine, if_exists='replace')
        df_mlife.to_sql('testapp_auroramlife', con=engine, if_exists='replace')
        df_tps.to_sql('testapp_auroratps', con=engine, if_exists='replace')
        df_aris.to_sql('testapp_auroraaris', con=engine, if_exists='replace')


        cursor = engine.cursor()
        cursor.execute("DELETE fROM testapp_auroradistribution")
        cursor.execute("DELETE FROM SQLITE_SEQUENCE WHERE name='testapp_auroradistribution'")
        engine.commit()
        cursor.close()

        for x in df_dist.itertuples():
            x = auroradistribution.objects.create(Agent=x.Agent, transcount=x.transCount,avgResponseTime=x.avgResponseTime, medResponseTime=x.medResponseTime,maxResponseTime=x.maxResponseTime)
            x.save()

        return render(request, 'testapp/aurorainput.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'testapp/aurorainput.html')


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print("File name" + filename)
        print("file URL" + uploaded_file_url )
        str(BASE_DIR) + "/media/"
        Filelocation=str(BASE_DIR) + "/media/" + str(filename)
        print("fileLocation" + Filelocation)
        while not os.path.exists(Filelocation):
            time.sleep(1)
        engine = sqlite3.connect(str(BASE_DIR) + "/" + 'db.sqlite3')
        [df1, df2, df3, df4, df5, df6, df7, df8] = processMobileLogs(Filelocation)

        df1.to_sql('testapp_endpointavgtime', con=engine, if_exists='replace')
        df2.to_sql('testapp_endpointavgtime1', con=engine, if_exists='replace')
        df3.to_sql('testapp_endpointavgtime2', con=engine, if_exists='replace')
        df4.to_sql('testapp_endpointavgtime3', con=engine, if_exists='replace')
        df5.to_sql('testapp_endpointavgtime4', con=engine, if_exists='replace')
        df6.to_sql('testapp_endpointavgtime5', con=engine, if_exists='replace')
        df7.to_sql('testapp_endpointavgtime6', con=engine, if_exists='replace')
        df8.to_sql('testapp_endpointavgtime7', con=engine, if_exists='replace')

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
        time = endpointavgtime.objects.values_list("averageResponseTime", flat=True)
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
        time = endpointavgtime1.objects.values_list("averageResponseTime", flat=True)
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
        time = endpointavgtime2.objects.values_list("averageResponseTime", flat=True)
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
        time = endpointavgtime3.objects.values_list("averageResponseTime", flat=True)
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
        time = endpointavgtime4.objects.values_list("averageResponseTime", flat=True)
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
        endpoint = endpointavgtime5.objects.values_list("level", flat=True)
        time = endpointavgtime5.objects.values_list("transactionCount", flat=True)
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
        time = endpointavgtime6.objects.values_list("transactionCount", flat=True)
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
        time = endpointavgtime7.objects.values_list("transactionCount", flat=True)
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



class auroradata1(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        transcount=auroraaggregate.objects.values_list("transcount", flat=True)
        agentleg=auroraaggregate.objects.values_list("Agent", flat=True)
        avgResponseTime = auroraaggregate.objects.values_list("avgResponseTime", flat=True)
        medResponseTime = auroraaggregate.objects.values_list("medResponseTime", flat=True)
        maxResponseTime = auroraaggregate.objects.values_list("maxResponseTime", flat=True)
        data = {
                "transcount":transcount,
                "agentleg": agentleg,
                "avgResponseTime": avgResponseTime,
                "medResponseTime":medResponseTime,
                "maxResponseTime":maxResponseTime,
        }
        return Response(data)

class auroradata2(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        transcount = auroraice.objects.values_list("transcount", flat=True)
        agentleg =auroraice.objects.values_list("Agent", flat=True)
        avgResponseTime = auroraice.objects.values_list("avgResponseTime", flat=True)
        medResponseTime = auroraice.objects.values_list("medResponseTime", flat=True)
        maxResponseTime = auroraice.objects.values_list("maxResponseTime", flat=True)
        data = {
                "transcount": transcount,
                "agentleg": agentleg,
                "avgResponseTime": avgResponseTime,
                "medResponseTime":medResponseTime,
                "maxResponseTime":maxResponseTime,
        }
        return Response(data)

class auroradata3(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        transcount = auroratps.objects.values_list("transcount", flat=True)
        agentleg = auroratps.objects.values_list("Agent", flat=True)
        avgResponseTime = auroratps.objects.values_list("avgResponseTime", flat=True)
        medResponseTime = auroratps.objects.values_list("medResponseTime", flat=True)
        maxResponseTime = auroratps.objects.values_list("maxResponseTime", flat=True)
        data = {
                "transcount": transcount,
                "agentleg": agentleg,
                "avgResponseTime": avgResponseTime,
                "medResponseTime":medResponseTime,
                "maxResponseTime":maxResponseTime,
        }
        return Response(data)

class auroradata4(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        transcount = auroraaris.objects.values_list("transcount", flat=True)
        agentleg = auroraaris.objects.values_list("Agent", flat=True)
        avgResponseTime = auroraaris.objects.values_list("avgResponseTime", flat=True)
        medResponseTime = auroraaris.objects.values_list("medResponseTime", flat=True)
        maxResponseTime = auroraaris.objects.values_list("maxResponseTime", flat=True)
        data = {
                "transcount": transcount,
                "agentleg": agentleg,
                "avgResponseTime": avgResponseTime,
                "medResponseTime":medResponseTime,
                "maxResponseTime":maxResponseTime,
        }
        return Response(data)

class auroradata6(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        transcount = auroradmp.objects.values_list("transcount", flat=True)
        agentleg = auroradmp.objects.values_list("Agent", flat=True)
        avgResponseTime = auroradmp.objects.values_list("avgResponseTime", flat=True)
        medResponseTime = auroradmp.objects.values_list("medResponseTime", flat=True)
        maxResponseTime = auroradmp.objects.values_list("maxResponseTime", flat=True)
        data = {
                "transcount": transcount,
                "agentleg": agentleg,
                "avgResponseTime": avgResponseTime,
                "medResponseTime":medResponseTime,
                "maxResponseTime":maxResponseTime,
        }
        return Response(data)


class auroradata7(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        transcount = auroramlife.objects.values_list("transcount", flat=True)
        agentleg = auroramlife.objects.values_list("Agent", flat=True)
        avgResponseTime = auroramlife.objects.values_list("avgResponseTime", flat=True)
        medResponseTime = auroramlife.objects.values_list("medResponseTime", flat=True)
        maxResponseTime = auroramlife.objects.values_list("maxResponseTime", flat=True)
        data = {
            "transcount": transcount,
            "agentleg": agentleg,
            "avgResponseTime": avgResponseTime,
            "medResponseTime": medResponseTime,
            "maxResponseTime": maxResponseTime,
        }
        return Response(data)

class PersonTable(tables.Table):
    class Meta:
        model = auroradistribution
        template_name = 'django_tables2/bootstrap.html'

def disttribution(request):
    table = PersonTable(auroradistribution.objects.all())

    RequestConfig(request).configure(table)
    return render(request, 'testapp/auroragraph5.html', {'table': table})


def auroragraph1(request):
    return render(request, 'testapp/auroragraph1.html')


def auroragraph2(request):
    return render(request, 'testapp/auroragraph2.html')


def auroragraph3(request):
    return render(request, 'testapp/auroragraph3.html')


def auroragraph4(request):
    return render(request, 'testapp/auroragraph4.html')

def auroragraph5(request):
    return render(request, 'testapp/auroragraph5.html')

def auroragraph6(request):
    return render(request, 'testapp/auroragraph6.html')

def auroragraph7(request):
    return render(request, 'testapp/auroragraph7.html')

def alertlogupload(request):
    if 'x' and 'y' and 'z' in request.GET:
        #message = 'You searched for: %r' % request.GET['x'] + request.GET['y']
        a=request.GET['x']
        b=request.GET['y']
        c=request.GET['z']
        print(a)
        filename = "AuroraAlertLogsSummary.xlsx"
        fs = FileSystemStorage()
        uploaded_file_url = fs.url(filename)

        engine = sqlite3.connect(str(BASE_DIR) + "/" + 'db.sqlite3')
        [df_server_summ, df_err_server_summ, df_method_server_summ, df_err_method_server_summ] = generateSummary(str(BASE_DIR) + "/media/AuroraAlertLogsSummary.xlsx",a,b,c)


        cursor = engine.cursor()
        cursor.execute("DELETE fROM testapp_aurorasummary")
        cursor.execute("DELETE FROM SQLITE_SEQUENCE WHERE name='testapp_aurorasummary'")
        engine.commit()
        cursor.close()

        for x in df_server_summ.itertuples():
            x = aurorasummary.objects.create(server=x.server, timeStamp=x.timeStamp)
            x.save()

        return render(request, 'testapp/alertlogupload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'testapp/alertlogupload.html')

class auroraanalysis(tables.Table):
    class Meta:
        model = aurorasummary
        template_name = 'django_tables2/bootstrap.html'

def alertloganalysis(request):
    table = auroraanalysis(aurorasummary.objects.all())

    RequestConfig(request).configure(table)
    return render(request, 'testapp/alertloganalysis.html', {'table': table})

def viz_details111(request):
    options = []
    headers = ["abc","cde","efg"]
    for header in headers:
        options.append((header, header))

    if request.method == 'POST':
        form = VizInfoForm(options, request.POST)
        #doesnt' get into the if statement since form is empty!
        #choices are not bounded to the model although the form is perfectly rendered
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/upload')
    else:
        #this works just fine
        form1 = VizInfoForm(options)
        return render(request, 'testapp/render_country.html', {'form1': form1})

def viz_details(request):
    options = []
    headers = ["abc", "cde", "efg"]
    for header in headers:
        options.append((header, header))
    if request.method == 'POST':
        form = VizInfoForm(options, request.POST)
        if form.is_valid():
            countries = form.cleaned_data.get('tog')
            form1 = countries
            return render(request, 'testapp/render_country.html', {'form1': form1})

    else:
        form = VizInfoForm(options)
        return render(request, 'testapp/render_country.html', {'form': form})

def countries_view(request):
    options = []
    headers = ["abc", "cde", "genesis","David"]
    for header in headers:
        options.append((header, header))
    if request.method == 'GET':
        form = CountryForm(options,request.GET)
        print("form")
        print(form)
        if form.is_valid():
            countries = form.cleaned_data.get('reasons_for_childcare')
            form.save()
            print("views---")
            print(countries)
            form1=countries
            return render(request, 'testapp/render_country.html', {'form1': form1})

    else:
        form = CountryForm(request.POST)
    return render(request, 'testapp/render_country.html',{'form': form})



# def some_view(request):
#     if request.method == 'POST':
#         form = SomeForm(request.POST)
#         if form.is_valid():
#             picked = form.cleaned_data.get('picked')
#             print(picked)
#     else:
#         form = SomeForm
#
#     return render(request,'testapp/render_country.html', {'form':form })


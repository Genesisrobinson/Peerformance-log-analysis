from django.template.loader import get_template
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.template import loader
from django.http import Http404
from .fileoperations import fileop
from .MGMautomatio import final



import json

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

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
            list=fileop(a,b)
            #print(list)
        else:
            list = final(a, b)
            message = 'not matchin'
    logs1 = {'name':[list],}

    #return HttpResponse(logs)
    return render_to_response("testapp/search_form1.html", {'logs1': logs1})









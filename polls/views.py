from django.shortcuts import render
from django.http import HttpResponse
def form(request):
    return  render(request,"polls/form.html",{})

def upload(request):
    for count, x in enumerate(request.FILES.getlist("files")):
      def process(f):
        with open('/Webapp/mysite/medial/file_' +str(count), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

      process(x)
    return HttpResponse("Files uploaded")






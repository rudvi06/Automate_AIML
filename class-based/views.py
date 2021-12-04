from django.shortcuts import render
from django.views import View

# Create your views here.
from django.shortcuts import render
from .forms import UploadFileForm
import mimetypes
from django.http import HttpResponse
#from django.http import FileResponse
#from django.core.files import File
#from django.contrib.staticfiles import finders
#from .models import Files
import pandas as pd

class upload_file(View):

    def handle_uploaded_file(f):
        '''with open('aiml_automate/endo.aiml', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)'''

        '''object=Files.objects.create(file='aiml/endo.aiml')
        object.save()'''

        df = pd.read_csv(f)
        f = open("aiml_automate/endo.aiml", "w")
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\
        <aiml version=\"1.0\">\n")

        for index in range(df['intent'].size):
            f.write("<category>\n<pattern>")
            f.write(df.iloc[index]['intent'].upper())
            f.write("</pattern>\n<template>")
            f.write(df.iloc[index]['answer'])
            f.write("</template>\n</category>\n")

        f.write("</aiml>")
        f.close()

    def get(self,request):
        text='Enter the file here'
        form = UploadFileForm()
        return (request, 'aiml_automate/index.html', {'form': form, 'text': text })

    def post(self,request):
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            upload_file.handle_uploaded_file(request.FILES['file'])
        t1='Your file is - '
        t2='<button type="submit" name="download" value="download" >Download</button>'
        text=t1+t2
        return (request, 'aiml_automate/index.html', {'form': form, 'text': text })


class download_file(View):
    def get(self,request):
        #text='Enter the file here'
        form = UploadFileForm()
        t1='Your file is - '
        t2='<button type="submit" name="download" value="download" >Download</button>'
        text=t1+t2
        return render(request, 'aiml_automate/index.html', {'form': form, 'text': text })

    def post(self,request):
        '''obj = Files.objects.get(id=6)
        filename = obj.file.path
        response = FileResponse(open(filename, 'rb'))
        return response'''

        fl_path = 'aiml_automate/'
        filename = 'endo.aiml'
        fl = open(fl_path+filename, 'r')
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

class automate(upload_file,download_file):
    def get(self,request):
        response=upload_file.get(self,request)
        return render(response[0],response[1],response[2])

    def post(self,request):
        if 'Submit' in request.POST:
            response=upload_file.post(self,request)
            return render(response[0],response[1],response[2])
        elif 'download' in request.POST:
            response=download_file.post(self,request)
            return response
        else:
            response=upload_file.get(self,request)
            return render(response[0],response[1],response[2])

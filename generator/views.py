from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from .sub_titles_generator import audio_to_text
from django.http import HttpResponse, Http404

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def upload(request):
    

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        result_path ='/results.txt/'
        file_path = BASE_DIR + uploaded_file_url
        print(BASE_DIR + uploaded_file_url)
        audio_to_text(file_path)

        context = {
            'uploaded_file_url': uploaded_file_url,
            'result_path' : result_path
        }


        return render(request, 'generator/upload.html', context)
    return render(request, 'generator/upload.html')


def download(request):
    
    file_path = BASE_DIR + '/results.txt'
    print(file_path)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from .sub_titles_generator import audio_to_text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def upload(request):
    

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        file_path = BASE_DIR + uploaded_file_url
        print(BASE_DIR + uploaded_file_url)
        audio_to_text(file_path)


        return render(request, 'generator/upload.html', { 'uploaded_file_url': uploaded_file_url })
    return render(request, 'generator/upload.html')

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from .sub_titles_generator import audio_to_text, force_align
from django.http import HttpResponse, Http404

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def upload(request):
    
    # TODO: remove spaces from file name

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']

        if myfile.name[-4:] ==  '.wav':
            myfile.name = 'uploaded_file.wav'
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            result_path ='/results.txt/'
            file_path = BASE_DIR + uploaded_file_url
            print(BASE_DIR + uploaded_file_url)
            audio_to_text(file_path)
            force_align(file_path, BASE_DIR + '/results.txt', BASE_DIR)

            context = {
                'uploaded_file_url': uploaded_file_url,
                'result_path' : result_path
            }


            return render(request, 'generator/upload.html', context)
        else:
            return HttpResponse( 'unsupported file format')
    return render(request, 'generator/upload.html')


def download(request):
    
    # file_path = BASE_DIR + '/results.txt'
    file_path = BASE_DIR + '/syncmap.srt'
    print(file_path)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404

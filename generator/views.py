from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from .sub_titles_generator import audio_to_text, force_align
from django.http import HttpResponse, Http404
import subprocess
from django.contrib import messages


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def upload(request):
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']

            if myfile.name[-4:] ==  '.mp3':
                # convert mp3 to wav
                myfile.name = 'uploaded_file.mp3'
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                file_path = BASE_DIR + uploaded_file_url
                path_to_wav_file = file_path[:-4] + '.wav'
                subprocess.call(['ffmpeg', '-i', file_path,  path_to_wav_file])
                audio_to_text(path_to_wav_file)
                force_align(path_to_wav_file, BASE_DIR + '/results.txt', BASE_DIR)
                context = {
                    'uploaded_file_url': uploaded_file_url,
                    'uploaded_successfully' : True
                }
                messages.success(request, 'SRT file successfully generated, your file won\'t be stored in our systems')
                return render(request, 'generator/upload.html', context)

            if myfile.name[-4:] ==  '.wav':
                myfile.name = 'uploaded_file.wav'
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                file_path = BASE_DIR + uploaded_file_url
                audio_to_text(file_path)
                force_align(file_path, BASE_DIR + '/results.txt', BASE_DIR)
                context = {
                    'uploaded_file_url': uploaded_file_url,
                    'uploaded_successfully' : True
                }
                return render(request, 'generator/upload.html', context)

            if myfile.name[-4:] is not   '.mp3' and myfile.name[-4:] is not  '.wav':
                return HttpResponse( 'unsupported file format')

        return render(request, 'generator/upload.html')
    except:
        messages.warning(request, 'make sure you selected the right file')
        return render(request, 'generator/upload.html')  

def download(request):
    
    file_path = BASE_DIR + '/syncmap.srt'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404

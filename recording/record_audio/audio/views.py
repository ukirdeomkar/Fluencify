from django.shortcuts import render
from .models import Audio
from django.views.decorators.csrf import csrf_protect


# def upload_audio(request):
#     if request.method == 'POST':
#         audio = Audio(file=request.FILES['audio'])
#         audio.save()
#         return render(request, 'success.html')
#     return render(request, 'upload_audio.html')

def record_audio(request):
    return render(request, 'record_audio.html')
import os
from django.http import JsonResponse
from django.conf import settings

from django.shortcuts import render
from django.http import HttpResponse

@csrf_protect
def save_audio(request):
    if request.method == 'POST':
        audio = request.FILES['audio']
        with open('save/audio.mp3', 'wb+') as f:
            for chunk in audio.chunks():
                f.write(chunk)
        return HttpResponse('Audio saved successfully')
    return HttpResponse('Error saving audio')
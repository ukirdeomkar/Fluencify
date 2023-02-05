from django.shortcuts import render
from .models import Audio
from django.views.decorators.csrf import csrf_protect
import wave
import numpy as np
import librosa
import os
import pdb 
import time 
import pickle 
model = pickle.load(open('model/mlp_300_32.sav', 'rb'))


def feature_extraction(file_name):
    # pdb.set_trace()
    #X, sample_rate = sf.read(file_name, dtype='float32')
    X , sample_rate = librosa.load(file_name, sr=None) 
    if X.ndim > 1:
        X = X[:,0]
    X = X.T
    
    ## stFourier Transform
    stft = np.abs(librosa.stft(X))
            
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=20).T, axis=0) 
    rmse = np.mean(librosa.feature.rms(y=X).T, axis=0) 
    spectral_flux = np.mean(librosa.onset.onset_strength(y=X, sr=sample_rate).T, axis=0) 
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=X).T, axis=0)
    
    return mfccs, rmse, spectral_flux, zcr


def feature_out(predict_path):
    # pdb.set_trace()
    n_mfccs = 20 
    number_of_features = 3 + n_mfccs
    features = np.empty((0,number_of_features))
    mfccs, rmse, spectral_flux, zcr = feature_extraction(predict_path)
    extracted_features = np.hstack([mfccs, rmse, spectral_flux, zcr])
    features_predict = np.vstack([features, extracted_features])
    return features_predict


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
    # pdb.set_trace()
    if request.method == 'POST':
        audio = request.FILES['audio']
        with open('save/audio.mp3', 'wb+') as f:
            for chunk in audio.chunks():
                f.write(chunk)
        for i in range(30):
            time.sleep(1)
            print(i)
        predict_path = 'save/audio.mp3'
        features_predict = feature_out(predict_path)
        prediction = model.predict(features_predict)

        print("\n\nThe Features is ",features_predict,"\n\n")
        print("\n\nThe Fluency Level is ",prediction,"\n\n")

        # os.remove("save/audio.mp3")
        return HttpResponse('Audio saved successfully')
    return HttpResponse('Error saving audio')





# --------------------------------------


    





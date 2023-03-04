from django.shortcuts import render,reverse,redirect,HttpResponseRedirect
from users_app.models import UserAdditionalModel
from main_app.models import Room
from django.contrib.auth.models import User
from django.db.models import Q
from fuzzywuzzy.fuzz import partial_token_set_ratio
import random

import os
from django.http import JsonResponse
from .models import Paragraph
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
import wave
import numpy as np
import librosa
import os
import pdb 
import time 
import pickle 
# model = pickle.load(open('model/mlp_300_32.sav', 'rb'))


def home(request):
    context = {}
    if request.user.is_authenticated:
        print(request.user.id)
        context['user1_interest'] = UserAdditionalModel.objects.get(userid=request.user.id).interest.split(",")
        context['user1_fluency'] = UserAdditionalModel.objects.get(userid=request.user.id).fluency
        print(context['user1_interest'])
        return render(request,'home2.html',context)
    return redirect('login')


def roomdetails(request,room):
    room_url = f'https://english-learn-meet-call.web.app/?id={room.room_id}'

    user1 = request.user
    user2 = room.user2 if room.user1 == user1 else room.user1
    
    context = {}
    context['room_url'] = room_url
    context['user1_interest'] = UserAdditionalModel.objects.get(userid=user1.id).interest
    context['user2_interest'] = UserAdditionalModel.objects.get(userid=user2.id).interest
    context['matched_user'] = user2.username
    context['matched_percentage'] = round(room.matching_percentage,2)
    context['common_interest'] = room.common_interest
    return render(request,'roomdetails.html',context)

def findparthner(request):

    #wait to avoid inconsistency
    # time.sleep(5)

    current_user = request.user
    room = Room.objects.filter(Q(user1=current_user) | Q(user2=current_user)).last()
    print(room)
    if room is not None:
        return roomdetails(request,room)

    user1 = UserAdditionalModel.objects.get(userid=current_user.id)
    user1_fluency = user1.fluency
    user1_interest_list = user1.interest.split(',')
    print(user1_interest_list)

    exclude_users = list(Room.objects.values_list('user1', flat=True)) + list(Room.objects.values_list('user1', flat=True))
    user_list = UserAdditionalModel.objects.exclude(userid__in=exclude_users).exclude(id=current_user.id)
    print(len(user_list))

    user2 = None 
    max_matched_percentage = 0
    max_matched_interest = []

    for user in user_list:
        print(f"Matching with {user1.userid}")
        if user.userid.id == user1.userid.id:
            continue
        user2_interest_list = user.interest.split(',')
        matched_interest_count = 0
        matched_interest = []
        for interest1 in user1_interest_list:
            for interest2 in user2_interest_list:
                if partial_token_set_ratio(interest1,interest2) > 90:
                    print(interest1,interest2)
                    matched_interest.append(interest1)
                    matched_interest_count += 1
                    break
        user1_matched_percentage = (matched_interest_count/len(user1_interest_list))*100
        user2_matched_percentage = (matched_interest_count/len(user2_interest_list))*100
        print(f"Matching with {user.userid.username} User 1 Matched {user1_matched_percentage}, \
              User 2 Matched {user2_matched_percentage}")
        if user1_matched_percentage >= 50 and user2_matched_percentage >= 50:
            max_matched_percentage = user1_matched_percentage
            user2 = user
            max_matched_interest = matched_interest
            if max_matched_percentage > 50:
                break 
            
    import pdb;pdb.set_trace()
    if user2 == None:
        return HttpResponse('No Match Found! Please Try Again After Sometime')
    
    common_interest = ','.join(max_matched_interest)
    ruser1 = User.objects.get(id=user1.userid.id)
    ruser2 = User.objects.get(id=user2.userid.id)

    room_id = random.randint(1000,9999)
    room = Room.objects.create(user1=ruser1 , user2=ruser2 , room_id=room_id , 
                            common_interest=common_interest,matching_percentage=max_matched_percentage)

    return roomdetails(request,room)

# Fluency++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



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

@csrf_protect
def check_fluency(request):
    if request.method == 'POST':
        
        audio = request.FILES['audio']
        with open('save/audio.mp3', 'wb+') as f:
            for chunk in audio.chunks():
                f.write(chunk)
        # for i in range(30):
        #     time.sleep(1)
        #     print(i)
        # predict_path = 'save/audio.mp3'
        # features_predict = feature_out(predict_path)
        # prediction = model.predict(features_predict)

        # print("\n\nThe Features is ",features_predict,"\n\n")
        # ans = np.argmax(prediction[0]) + 1
        # ans =int(ans)
        # temp = UserAdditionalModel.objects.filter(userid=request.user.id)
        # previous_fluency = None
        # if temp != None:
        #     previous_fluency = temp.first().fluency
            
        # print(f'\n\nYour Previous fluency is {previous_fluency}')
        # print("\n\nThe Fluency Level is ",ans,"\n\n")
        # # UserAdditionalModel.objects.get(userid=request.user.id).update(fluency = ans)
        # user_temp = UserAdditionalModel.objects.get(userid=request.user.id)
        # user_temp.fluency = ans 
        # user_temp.save()

        prediction = "1"

        return JsonResponse({'fluency': prediction})
     
    user_fluency = UserAdditionalModel.objects.filter(userid=request.user.id).first().fluency
    random_paragraph = Paragraph.objects.order_by('?').first().paratext
    context = {}
    context["user_fluency"] = user_fluency
    context["paragraph"] = random_paragraph
    return render(request, 'fluencycheck.html',context=context)



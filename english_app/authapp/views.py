from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.http import *
from django.contrib import messages
from .models import addtionalInfoModel

import nltk
# nltk.download('wordnet')
# nltk.download('omw-1.4')
from nltk.stem import PorterStemmer
from fuzzywuzzy.fuzz import partial_token_set_ratio
import random

def steminize(interest_str):
    ps = PorterStemmer()
    interest_list = interest_str.strip().split(',')
    interest_processed = [ps.stem(inst) for inst in interest_list]
    processed_interest_str = ','.join(interest_processed)
    return processed_interest_str

def signup(request):
    if request.method == "POST":
        data = request.POST
        name = data['name']
        username = data['username']
        password = data['password']
        confirm_password = data['confirm_password']
        age = data['age']
        interest_str = data['interest']

        user = User.objects.filter(username=username).exists()
        if not user :
            if password == confirm_password:
                user = User.objects.create_user(username=username,password=password,first_name=name)
                interest_str = steminize(interest_str)
                addtionalInfoModel.objects.update_or_create(userid=user,interest=interest_str,age=age)
                return redirect("login")
            else:
                messages.error(request,"Password does not match")
                return redirect('signup')
        else:
            messages.error(request, "Username already exist")
            return redirect('signup')

    return render(request,"signup.html")

def login(request):
    if request.method == "POST":
        data = request.POST
        username = data['username']
        password = data['password']

        user = authenticate(request,username=username,password=password)
        if user is not None:
            auth_login(request,user)
            return redirect("home")
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('login')
    return render(request,"login.html")

def logout(request):
    auth_logout(request)
    return redirect("login")


def home(request):
    context = {}
    if request.user.is_authenticated:
        print(request.user.id)
        current_interest = addtionalInfoModel.objects.get(userid=request.user.id).interest
        # print(current_interest)
        context['current_interest'] = current_interest
        return render(request,'home.html',context)
    return redirect(login)


def update(request):
    if request.method == 'POST':
        updated_interest = steminize(request.POST['updated_interest'])
        addtionalInfoModel.objects.filter(userid=request.user).update(interest=updated_interest)
    return redirect(home)

def findparthner(request):
    # import pdb;pdb.set_trace()
    user1_id = request.user.id
    user1 = addtionalInfoModel.objects.get(userid=user1_id)
    target_fluency = user1.fluency

    user1_interest_list = user1.interest.split(',')
    print(user1_interest_list)
    user_list = addtionalInfoModel.objects.filter(fluency=target_fluency)
    
    # max_matched_user = None
    user2 = None 
    max_matched_percentage = 0
    max_matched_interest = []

    for user in user_list:
        print(user.userid.id,user1_id)
        if user.userid.id == user1_id:
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
        matched_interest_percentage = (matched_interest_count/len(user1_interest_list))*100
        print(user.userid.username,matched_interest_percentage)
        if matched_interest_percentage > max_matched_percentage:
            max_matched_percentage = matched_interest_percentage
            user2 = user
            max_matched_interest = matched_interest
        if matched_interest_percentage > 50:
            user2 = user
            max_matched_interest = matched_interest
            break

    context = {}
    context['user1_interest'] = user1.interest
    context['user2_interest'] = addtionalInfoModel.objects.get(userid=user2.userid).interest
    context['user2'] = user2.userid
    context['matched_percentage'] = round(max_matched_percentage,2)
    context['common_interest'] = ','.join(max_matched_interest)
    return render(request,'home.html',context)

    room_id = random.randint(1000,9999)
    room_url = f'https://english-learn-meet-call.web.app/?id={room_id}'
    return redirect(room_url)


# def findparthner2(request):
#     # import pdb;pdb.set_trace()
#     user_id = request.user.id
#     user_additional_info = addtionalInfoModel.objects.get(userid=user_id)
#     user_interest = set(user_additional_info.interest.split(","))
#     user_fluency = user_additional_info.fluency
#     max_score = 0
#     best_user = -1
#     commom_interest = set()
#     isFound = False
#     user = addtionalInfoModel.objects.filter(fluency=user_fluency)
#     print(user)
#     for u in user:
#         if user_id == u.userid.id or user_fluency < u.fluency:
#             continue
#         score = 0
#         u_interest = set(u.interest.split(','))
#         # print(u_interest)
#         matched = user_interest.intersection(u_interest)
#         # print(matched)
#         score = (len(matched)/len(user_interest))*100
#         print(f"user {u.id} matched {score}%")
#         print(u_interest,user_interest)
#         if max_score < score:
#             best_user = u.userid
#             max_score = score
#             commom_interest = matched
#             if max_score >= 50:
#                 isFound = True
#         if isFound:
#             break
#     print(best_user,max_score,commom_interest)

#     context = {}
#     current_interest = addtionalInfoModel.objects.get(userid=request.user.id).interest
#     context['user_fluency'] = user_fluency
#     context['current_interest'] = current_interest
#     context['best_user'] = best_user
#     context['matched_percentage'] = round(max_score,2)
#     context['common_interest'] = commom_interest
#     return render(request,'home.html',context)



# ------------------------------------------------------Fuck off-------------------------

from django.shortcuts import render
# from .models import Audio
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


import os
from django.http import JsonResponse
from django.conf import settings

from django.shortcuts import render
from django.http import HttpResponse


def record_audio(request):
    return render(request, 'record_audio.html')



@csrf_protect
def save_audio(request):
    # pdb.set_trace()
    if request.method == 'POST':
        audio = request.FILES['audio']
        with open('save/audio.mp3', 'wb+') as f:
            for chunk in audio.chunks():
                f.write(chunk)
        # for i in range(30):
        #     time.sleep(1)
        #     print(i)
        predict_path = 'save/audio.mp3'
        features_predict = feature_out(predict_path)
        prediction = model.predict(features_predict)

        print("\n\nThe Features is ",features_predict,"\n\n")
        ans = np.argmax(prediction[0]) + 1
        ans =int(ans)
        print(f'\n\nYour Previous fluency is {addtionalInfoModel.objects.get(userid=request.user.id).fluency}')
        print("\n\nThe Fluency Level is ",ans,"\n\n")
        # addtionalInfoModel.objects.get(userid=request.user.id).update(fluency = ans)
        user_temp = addtionalInfoModel.objects.get(userid=request.user.id)
        user_temp.fluency = ans 
        user_temp.save()

        # os.remove("save/audio.mp3")
        return HttpResponse('Audio saved successfully')
    return HttpResponse('Error saving audio')





# --------------------------------------


    






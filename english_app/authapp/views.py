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


def getMatch(user1_id,target_fluency):
    import pdb;pdb.set_trace()
    user1 = addtionalInfoModel.objects.get(userid=user1_id)
    user1_interest = user1.interest
    print(user1_interest)
    user_list = addtionalInfoModel.objects.filter(fluency=target_fluency)
    user2 = None 
    
    max_matched_user = None
    max_matched_percentage = 0

    for user in user_list:
        user2_interest = user.interest
        matched_interest_count = 0
        for interest1 in user1_interest:
            for interest2 in user2_interest.split(','):
                if partial_token_set_ratio(interest1,interest2) > 90:
                    print(interest1,interest2)
                    matched_interest_count += 1
        matched_interest_percentage = (matched_interest_count/len(user1_interest))*100
        print(user,matched_interest_percentage)
        if matched_interest_percentage > max_matched_percentage:
            max_matched_percentage = matched_interest_percentage
            max_matched_user = user
        if matched_interest_percentage > 50:
            return user.userid,matched_interest_percentage
    return max_matched_user.userid,max_matched_percentage
        



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


def findparthner2(request):
    # import pdb;pdb.set_trace()
    user_id = request.user.id
    user_additional_info = addtionalInfoModel.objects.get(userid=user_id)
    user_interest = set(user_additional_info.interest.split(","))
    user_fluency = user_additional_info.fluency
    max_score = 0
    best_user = -1
    commom_interest = set()
    isFound = False
    user = addtionalInfoModel.objects.filter(fluency=user_fluency)
    print(user)
    for u in user:
        if user_id == u.userid.id or user_fluency < u.fluency:
            continue
        score = 0
        u_interest = set(u.interest.split(','))
        # print(u_interest)
        matched = user_interest.intersection(u_interest)
        # print(matched)
        score = (len(matched)/len(user_interest))*100
        print(f"user {u.id} matched {score}%")
        print(u_interest,user_interest)
        if max_score < score:
            best_user = u.userid
            max_score = score
            commom_interest = matched
            if max_score >= 50:
                isFound = True
        if isFound:
            break
    print(best_user,max_score,commom_interest)

    context = {}
    current_interest = addtionalInfoModel.objects.get(userid=request.user.id).interest
    context['user_fluency'] = user_fluency
    context['current_interest'] = current_interest
    context['best_user'] = best_user
    context['matched_percentage'] = round(max_score,2)
    context['common_interest'] = commom_interest
    return render(request,'home.html',context)



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
    user_id = request.user.id
    user_additional_info = addtionalInfoModel.objects.get(userid=user_id)
    user_interest = set(user_additional_info.interest.split(","))
    user_fluency = user_additional_info.fluency
    max_score = 0
    best_user = -1
    commom_interest = set()
    isFound = False
    same_level_user = addtionalInfoModel.objects.filter(fluency=user_fluency)
    same_level_user_id = []
    user = User.objects.all()
    print(user)
    for u in user:
        # print(u.id)
        u_addtional_info = addtionalInfoModel.objects.get(userid=u.id)
        if user_id == u.id or user_fluency < u_addtional_info.fluency:
            continue
        score = 0
        u_interest = set(u_addtional_info.interest.split(','))
        # print(u_interest)
        matched = user_interest.intersection(u_interest)
        # print(matched)
        score = (len(matched)/len(user_interest))*100
        print(f"user {u.id} matched {score}%")
        print(u_interest,user_interest)
        if max_score < score:
            best_user = u.id
            max_score = score
            commom_interest = matched
            if max_score >= 50:
                isFound = True
        if isFound:
            break
    print(best_user,max_score,commom_interest)
    return redirect('https://www.wikipedia.com')



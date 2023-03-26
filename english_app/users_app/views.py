from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.http import *
from django.contrib import messages
from .models import UserAdditionalModel
from main_app.models import Room
from django.db.models import Q

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
                # interest_str = steminize(interest_str)
                UserAdditionalModel.objects.update_or_create(userid=user,interest=interest_str,age=age)
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
        print(User.objects.get(username=username).password)
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


def update(request):
    # import pdb;pdb.set_trace()
    if request.method == 'POST':
        # updated_interest = steminize(request.POST['updated_interest'])
        updated_interest = request.POST['interestsDropdown']
        print(updated_interest)
        UserAdditionalModel.objects.filter(userid=request.user).update(interest=updated_interest)
        Room.objects.filter(Q(user1=request.user) | Q(user2=request.user)).delete()
    return redirect('home')
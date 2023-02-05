
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name='home'),
    path("login", views.login , name="login"),
    path("signup", views.signup , name="signup"),
    path("logout", views.logout , name="logout"),
    path("update", views.update , name="update"),
    path("findparthner", views.findparthner , name="findparthner"),
    path('record_audio', views.record_audio, name='record_audio'),
    path('save_audio/', views.save_audio, name='save_audio'),

]

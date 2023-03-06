from django.urls import path,include
from main_app.views import *

urlpatterns = [
    path('', home , name='home'),
    path("findparthner", findparthner , name="findparthner"),
    path('check_fluency', check_fluency, name='check_fluency'),
    # path("findother", findother , name="findother"),
    # path("login", include('users_app.urls')),
]

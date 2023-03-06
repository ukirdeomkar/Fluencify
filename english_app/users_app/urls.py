from django.urls import path,include
from users_app.views import *

urlpatterns = [
    path("login", login , name="login"),
    path("signup", signup , name="signup"),
    path("logout", logout , name="logout"),
    path("update", update , name="update"),
]

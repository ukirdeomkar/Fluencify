from . import views
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', views.upload_audio, name='upload_audio'),
    # path('', views.record_audio, name='record_audio'),
    path('', views.record_audio, name='record_audio'),
    path('save_audio/', views.save_audio, name='save_audio'),


]
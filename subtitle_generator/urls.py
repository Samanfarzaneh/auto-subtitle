# subtitle_generator/urls.py
from django.urls import path
from .views import upload_video

urlpatterns = [
    path('/', upload_video, name='upload_video'),
]

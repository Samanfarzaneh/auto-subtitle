# AutoSubtitle1/urls.py
from django.urls import path, include
from . import views
# AutoSubtitle1/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from subtitle_generator.views import autosub_404, upload_video



urlpatterns = [
    path('', views.subtitle_editor, name='upload_video'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

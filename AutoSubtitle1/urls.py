# AutoSubtitle1/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from subtitle_generator.views import autosub_404, upload_video


urlpatterns = [
    path('', upload_video, name='upload_video'),
    path('404/', autosub_404, name='404'),
    path('admin/', admin.site.urls),
    path('subtitle/', include('SubTitleEditor.urls'), name="subtitle_editor"),
]

handler404 = 'subtitle_generator.views.autosub404'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

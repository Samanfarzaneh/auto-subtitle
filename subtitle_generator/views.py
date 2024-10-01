import os
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import VideoUploadForm  # فرض بر این است که فرم آپلود ویدیو در forms.py تعریف شده است
from .subtitle_generator import generate_srt_from_video  # کدهای تولید زیرنویس شما


@csrf_exempt
def upload_video(request):
    srt_file_url = None  # متغیر برای ذخیره آدرس فایل زیرنویس
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['video']
            video_path = f'media/videos/{video_file.name}'

            # ذخیره فایل ویدیو
            with open(video_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

            # تولید زیرنویس
            srt_file_path = generate_srt_from_video(video_path)
            srt_file_name = f"{os.path.splitext(video_file.name)[0]}.srt"
            srt_file_url = f'/media/videos/{srt_file_name}'  # آدرس فایل زیرنویس
            print(srt_file_url)
            return render(request, 'upload_video.html', {'form': form, 'srt_file_url': srt_file_url})
    else:
        form = VideoUploadForm()  # در حالت GET، فرم را مقداردهی کنید
    #         if os.path.exists(srt_file_url):  # بررسی وجود فایل
    #             response = HttpResponse(open(srt_file_url, 'rb').read(), content_type='text/plain')
    #             response['Content-Disposition'] = f'attachment; filename="{srt_file_name}"'
    #             return response
    #         else:
    #             return HttpResponse("Subtitle file not found.", status=404)
    # print(srt_file_url)

    return render(request, 'upload_video.html', {'form': form, 'srt_file_url': srt_file_url})



def autosub404(request, exception):
    return render(request, '404.html', status=404)

def autosub_404(request):
    return render(request, '404.html')

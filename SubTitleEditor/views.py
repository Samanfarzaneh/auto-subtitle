from django.shortcuts import render

# Create your views here.
def subtitle_editor(request):
    return render(request, 'subtitle_editor.html')
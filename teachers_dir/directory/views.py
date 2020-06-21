from django.shortcuts import render

# Create your views here.
def directory(request):
    return render(request, 'directory/directory.html')
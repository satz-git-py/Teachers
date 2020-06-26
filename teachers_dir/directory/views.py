from django.shortcuts import render, get_object_or_404
from .models import Teacher
# import re
import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# view method to render the home page 'directory.html'
def directory(request):
    teachers = Teacher.objects.all()
    return render(request, 'directory/directory.html', {'teachers': teachers})

# view method to render the profile page for each teacher
def profile(request, teach_id):
    # check for the existence of the teacher instance
    teacher = get_object_or_404(Teacher, pk=teach_id)
    # actual url used to retrieve the existing images
    url = f'../../static/directory/img/{teacher.Profile_Picture}'
    # url used for validation pupose
    url_val = os.path.join(BASE_DIR, f'static/directory/img/{teacher.Profile_Picture}')
    # checking for the existence of the actual path of the image by replacing escape char in base_dir
    # check for existence of the profile picture, if not present default picture path will be assigned
    if not os.path.isfile(url_val.replace('\\', '/')):
        url = '../static/directory/img/no-pp.jpg'
    return render(request, 'directory/profile.html', {'teacher': teacher, 'url': url})

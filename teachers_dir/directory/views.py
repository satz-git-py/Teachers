from django.shortcuts import render, get_object_or_404
from .models import Teacher
#import re
import os

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Create your views here.
def directory(request):
    teachers = Teacher.objects.all()

    #temporay glue code till the model field validation happens
    #junk = [null, ' ', '']
    #valid_teachers = [ t for t in teachers if t.First_Name in junk or t.Last_Name in junk or t.Email_Address in junk]
    #pattern = "[a-z][A-Z][0-9]"
    #valid_teachers = [ t for t in teachers if re.match(pattern, t.Email_Address[:2])]
    return render(request, 'directory/directory.html', {'teachers':teachers})

def profile(request, teach_id):
    #check for the existence of the teacher instance 
    teacher = get_object_or_404(Teacher, pk=teach_id)

    # actual url used to retreive the existing images
    url = f'../../static/directory/img/{teacher.Profile_Picture}'

    # url used for validation pupose
    url_val = os.path.join(BASE_DIR, f'static/directory/img/{teacher.Profile_Picture}')

    # checking for the existence of the actual path of the image by replacing escape char in base_dir
    if not os.path.isfile(url_val.replace('\\', '/')):
        url = '../static/directory/img/no-pp.jpg'

    return render(request, 'directory/profile.html', {'teacher':teacher, 'url':url})


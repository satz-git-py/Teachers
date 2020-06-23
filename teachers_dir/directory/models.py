from django.db import models
#from .validators import *

# Create your models here.
class Teacher(models.Model):
    First_Name = models.CharField('First Name', max_length=60, blank=False)
    Last_Name = models.CharField('Last Name', max_length=60, blank=False)
    Profile_Picture = models.CharField('Profile Picture', max_length=50)
    Email_Address = models.EmailField('Email Address', max_length = 254, unique=True) 
    Phone_Number = models.CharField('Phone Number', max_length=31)
    Room_Number = models.CharField('Room Number', max_length=10)
    Subjects_Taught = models.CharField('Subjects Taught', max_length=300)

    def __str__(self):
        return f'{self.Last_Name}, {self.First_Name}'

#class subject(models.Model):

from django.db import models

# Create your models here.
class Teacher(models.Model):
    First_Name = models.CharField(max_length=60)
    Last_Name = models.CharField(max_length=60)
    Profile_Picture = models.CharField(max_length=50)
    Email_Address = models.EmailField(max_length = 254) 
    Phone_Number = models.CharField(max_length=31)
    Room_Number = models.CharField(max_length=10)
    #Subjects Taught
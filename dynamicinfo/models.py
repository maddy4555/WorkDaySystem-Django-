from django.db import models

# Create your models here.

from django.contrib.auth.models import User
import datetime
from django.utils import timezone

# Create your models here.
class Info(models.Model):
    username=models.CharField(max_length=50)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    Wfh_application=models.PositiveIntegerField(default=30)
    Leave_application=models.PositiveIntegerField(default=30)
    date=models.DateField(default=datetime.date.today)
    now_time=models.TimeField(default=timezone.now())
    
    def __str__(self):
        return str(self.username)

class Wfh(models.Model):
    fdate=models.DateField()  
    tdate=models.DateField()
    reason=models.CharField(max_length=200)
    author=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.author)    

class Leave(models.Model):
    fdate=models.DateField()  
    tdate=models.DateField()
    reason=models.CharField(max_length=200)
    author=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.author)

class Image(models.Model):
    image=models.ImageField(upload_to="dynamicinfo/images",null=True)  
    author=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)    

    def __str__(self):
        return str(self.author)  

type=(
    ("Work From Home","Work From Home"),
    ("Holiday","Holiday"),
)
class WfhRequest(models.Model):
    request_type=models.CharField(max_length=20,default="Work From Home")
    reason=models.CharField(max_length=200)
    author=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.author)

class HolidayRequest(models.Model):
    request_type=models.CharField(max_length=20,default="Holiday")
    reason=models.CharField(max_length=200)
    author=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)        

    def __str__(self):
        return str(self.author)
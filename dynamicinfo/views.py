from django.shortcuts import render

# Create your views here.

from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.core.mail import send_mail
from WorkDaySystem.settings import EMAIL_HOST_USER
from .models import Wfh,Leave,Info,Image,WfhRequest,HolidayRequest
import datetime




def index(request):
    return render(request,"index.html")

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect("/dynamicinfo/dashboard/")
        else:
            messages.info(request,'invalid credentials')   
            return redirect("/dynamicinfo/login/") 
    else:    
        return render(request,"login.html")

def registration(request):
    if request.method=='POST':
        first_name=request.POST['first_name']#html wala
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        image=request.POST['img']
    
        try:
            remember=request.POST['remember']
        except MultiValueDictKeyError:
            remember = False
        print(remember)    
        if remember=='on':
            user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password1)
            user.save()
            hello=Image(image=image,author=user)
            hello.save()
            user.save()
            host=Info(username=username,firstname=first_name,lastname=last_name,email=email)
            host.save()
            subject = 'Welcome to Our Organization'
            message = 'We wish you to enjoy our service which will deliver you comfort of applying leaves of Work From Home and Holiday.'
            recepient = email
            send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)    
            return redirect('/dynamicinfo/login/')
        
        else:
            messages.info(request,'Please accept the terms and privacy')
            return redirect("/dynamicinfo/registration/")
            
            #messages.info(request,'please agree') 
        
    else:
        return render(request,"registration.html")
     

def logout(request):
    auth.logout(request)
    return redirect('/dynamicinfo/')       


@login_required


def dashboard(request):
    user=request.user
    a=Info.objects.get(username=user)
    c=a.Wfh_application
    z=Info.objects.get(username=user)
    x=z.Leave_application
    r=Image.objects.get(author=user)
    params={'left':c,'middle':x,'right':r,'zero':0}

    return render(request,"dashboard.html",params)
#os.path.join(BASE_DIR,'templates')

def profile(request):
    user=request.user
    r=Image.objects.get(author=user)
    a=Info.objects.get(username=user)
    c=a.Wfh_application
    z=Info.objects.get(username=user)
    x=z.Leave_application
    hi={'left':c,'middle':x,'right':r}
    return render(request,"profile.html",hi)


def wfh(request):
    global user_id
    user_id=request.user.id
    user=request.user
    if request.method=='POST':
        fdate=request.POST['fdate']#html wala
        tdate=request.POST['tdate']
        reason=request.POST['reason']
        
        
        year, month, day = map(int, fdate.split('-'))
        
        year1, month1, day1 = map(int, tdate.split('-'))
        date1 = datetime.date(year, month, day)
        date2 = datetime.date(year1, month1, day1)
        l=(date2-date1).days
        
        if(1<=l<=3):

            post=Wfh(fdate=fdate,tdate=tdate,reason=reason,author=user)
        
            post.save()
            a=Info.objects.get(username=user)
            c=a.Wfh_application
            c=c-1
            Info.objects.filter(username=user).update(Wfh_application=c)
            d=a.Wfh_application
            return redirect('/dynamicinfo/dashboard')
        else:
            messages.info(request,'You cannot apply for more than 3 days')
            return redirect("/dynamicinfo/wfh")
            

        
        
        #print(user_id)
        
    else:
        return render(request,"wfh.html")


def leave(request):
    global user_id
    user_id=request.user.id
    user=request.user
    if request.method=='POST':
        fdate=request.POST['fdate']#html wala
        tdate=request.POST['tdate']
        reason=request.POST['reason']
        year, month, day = map(int, fdate.split('-'))
        
        year1, month1, day1 = map(int, tdate.split('-'))
        date1 = datetime.date(year, month, day)
        date2 = datetime.date(year1, month1, day1)
        h=(date2-date1).days
        
        if(1<=h<=3):
            host=Leave(fdate=fdate,tdate=tdate,reason=reason,author=user)
            host.save()
            z=Info.objects.get(username=user)
            x=z.Leave_application
            x=x-1
            Info.objects.filter(username=user).update(Leave_application=x)
            v=z.Leave_application
            return redirect('/dynamicinfo/dashboard')
        else:
            messages.info(request,'You cannot apply for more than 3 days')
            return redirect("/dynamicinfo/leave")

    else:
        return render(request,"leave.html")  


def wfhrequest(request):
    user=request.user
    if request.method=='POST':
        reason=request.POST['reason']
        hi=WfhRequest(reason=reason,author=user)
        hi.save()
        return redirect('/dynamicinfo/dashboard')
    return render(request,'wfhrequest.html')          


def holidayrequest(request):
    user=request.user
    if request.method=='POST':
        reason=request.POST['reason']
        good=HolidayRequest(reason=reason,author=user)
        good.save()
        return redirect('/dynamicinfo/dashboard')
    return render(request,'holidayrequest.html')  
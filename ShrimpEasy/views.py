import datetime
import os
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.views import View
from .models import Farm,FarmDetails;
from datetime import datetime 
from decimal import Decimal


# Create your views here.


def home(request):
    if  request.user.is_authenticated:
        if request.method == 'GET':
         
           if 'farmName' in request.GET:


            farm_details , farms= GetFarm(request.user,request.GET['farmName'])
           else:
           
            farms , farm_details = initialGetFarm(request.user)
            if not farms:
                    return HttpResponseRedirect('addNewFarm')
        if request.META['HTTP_USER_AGENT'].find('Mobile') != -1:
            return render(request, 'home2.html',{'farm_details':farm_details , 'farms':farms})
        else:
            return render(request, 'home.html',{'farm_details':farm_details , 'farms':farms})
    else:        
        return redirect("login")


    
# def signup(req):
#     return render(req,"SignUp.html")

def signup(req):
    if req.method == 'POST':
        username=req.POST['username']
        email=req.POST['email']
        password1=req.POST['pass1']
        password=req.POST['pass2']
        if password == password1:
            if User.objects.filter(username=username).exists() | User.objects.filter( email=email).exists():
                error_message = "Email OR Username already exists. Please use a different one."
                return render(req, 'SignUp.html', {'error_message': error_message})
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user = auth.authenticate(username=username,password=password)
                auth.login(req,user)

                return redirect('addNewFarm')
        else:
            
            error_message = "Passwords do not match. Please try again."
            return render(req, 'SignUp.html', {'error_message': error_message})
    else:
        return render(req, 'SignUp.html')

def login (req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(req,user)
            return redirect('home')
        else:
            
            error_message = "Invalid Credentials"
            return render(req, 'login.html', {'error_message': error_message})

    else:
        return render(req,'login.html')
def logout(req):
    auth.logout(req)
    return redirect('login')
def addNewFarm(req):
    if req.method=='POST':
        user = req.user
        farmname=req.POST['farmName']
        date=req.POST['date']
        weight=req.POST['weight']
        pieces=req.POST['pieces']
        abw=req.POST['abw']
        gain=req.POST['gain']
        adg=req.POST['adg']

        try:
            new_farm = Farm.objects.create(user=user, name=farmname)
            print(new_farm)
            print("Created farm tyep",type(new_farm))
            FarmDetails.objects.create(farm=new_farm, date=date, weight=weight, piece=pieces, abw=abw, gain=gain, adg=adg)
            return redirect('home')
        except IntegrityError:
            return JsonResponse({'error': ('Farm already exists, Try With Different Farm Name')}, status=400)
    else:
        
        return render(req,'AddNewFarm.html')
    


def GetFarm(user,farmName):
    print(farmName)
    allFarms = Farm.objects.filter(user=user)

    to_array = [char for char in farmName]
    print(to_array)
    for f in allFarms:
        to_array = [char for char in f.name]
        print(to_array)

    farm = Farm.objects.filter(user=user,name=farmName)
    print("farm is :----",farm)
    print("allFarms is :----", farm[0])

    farm_details = FarmDetails.objects.filter(farm=farm[0].id )
    return farm_details ,allFarms

def initialGetFarm(user):
    farm_details = None
    farms = Farm.objects.filter(user=user)
    if  farms:
        farm_details = FarmDetails.objects.filter(farm=farms[0])
    return farms ,farm_details
def calculateProgress(req):
    user = req.user
    farm   = req.POST['farm']
    weight = int(req.POST['weight'])
    pieces = int(req.POST['pieces'])
    currentDate =  datetime.strptime(req.POST['date'], "%Y-%m-%d").date()


 
    
    farm_details  = GetFarm(user,farm)
    farm_details= farm_details[0].latest('date')
   
    
    prev_abw =farm_details.abw
    prev_date =  farm_details.date

    abw = Decimal(weight/pieces)
    print("type of prev abw , abw",type(prev_abw),type(abw))
    gain = abw -prev_abw
    day_gap = (currentDate - prev_date).days;
    adg = gain/day_gap;
    newRecord=FarmDetails(farm=farm_details.farm, date=currentDate, weight=weight, piece=pieces, abw=abw, gain=gain, adg=adg)
    if( newRecord.save() ):
        return HttpResponse('Error to insert new record')
    else:
        return redirect('/?farmName='+farm)

def deleteFarm(req):
  farm = Farm.objects.filter(user=req.user, name=req.POST["ToBeDeletedFarm"])
  farm.delete()

  return redirect('home')


def deleteRecord(req):
  FarmDetails, farm = GetFarm(req.user, req.GET['tobDeleteFarm'])
  FarmDetails.delete()

  return redirect('home')

def weather(req):
    from dotenv import load_dotenv
    load_dotenv()
    weatherApi=os.getenv('WeatherApi')
    return render(req, 'weather.html',{'api': weatherApi})
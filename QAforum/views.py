from django.shortcuts import render
import datetime
from models import *
from django.db.models import Max
from django.contrib.auth.models import User
from django.http import HttpResponse
# Create your views here.

def register(request):
    return render(request,'reg.html')

def login(request):
    return render(request,'login.html')
    
def home(request):
    
    question = Question.objects.aggregate(Max('id'))
    a = question['id__max']
    questlist = []
    for i in range(5):
        q = Question.objects.get(id=(a-i))
        questlist.append(q)
    return render(request,'home.html',{'l':questlist})

def display(request):
    return render(request,'post.html')
    
def question(request):
    if 'postt' in request.GET:
        quest = request.GET['quest']
        
        user_id= request.user.id
        user = User.objects.get(id = user_id)
        date_created = datetime.datetime.now()
        date_updated = datetime.datetime.now()
        obj = Question(title=quest,user_id=user,date_created=date_created,date_update=date_updated)
        obj.save()
        return HttpResponse("success")
        
        

    
        
        
        
        
           



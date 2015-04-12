from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render_to_response
import datetime
from models import *
from django.db.models import Max
from django.contrib.auth.models import User
from django.http import HttpResponse
from forms import UserForm, UserProfileForm, LoginForm, UpdateProfile, UpdateImage
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from helper import get_query
# Create your views here.

#def register(request):
 #   return render(request,'reg.html')

#def main(request):
 #   return render(request,'main.html')
 
def about(request):
    return render(request, 'about.html')
    
def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(request.POST,request.FILES)
       # p = UserProfileForm(data=request.FILES)
        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():# and p.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
               # p.picture = request.FILES['picture']
               # p.save()
               profile.picture = request.FILES['picture']
            # Now we save the UserProfile model instance.
            profile.save()
                
            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'registration.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    logged_in = False
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST' and not request.user.is_authenticated():
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        login_form = LoginForm(data=request.POST)
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/forum/home/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print login_form.errors
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    elif request.method == 'POST' and request.user.is_authenticated():
        return HttpResponseRedirect("/forum/home/")
    
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        login_form=LoginForm()
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {'login_form':login_form}, context)
        
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
    
# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/forum/login')
    
@login_required    
def profile(request):
    changed = ""
    msg = " "
    username=request.user.username
    fname=request.user.first_name
    lname=request.user.last_name
    email=request.user.email
    obj = User.objects.get(username=request.user.username)
    obj1 = UserProfile.objects.get(user=obj)
    if 'msg' in request.GET : 
        msg = request.GET['msg']
    if 'changed' in request.GET : 
        changed = request.GET['changed']
        

    return render_to_response('profile.html', { 'username':username, 'fname':fname,'lname':lname,'email':email,'obj1':obj1,'msg':msg,'changed':changed})
    
    

@login_required        
def update_profile(request):
    
    
    user = User.objects.get(pk=request.user.id)
    obj1 = UserProfile.objects.get(user=user)
    if request.POST:
        user = User.objects.get(pk=request.user.id)
        obj1 = UserProfile.objects.get(user=user)
        user.first_name=request.POST.get('first_name')
        user.last_name=request.POST.get('last_name')
        user.username=request.POST.get('username')                    
        user.email=request.POST.get('email') 
        obj1.picture= request.FILES['picture']
        obj1.website= request.POST.get('website')
        
        user.save()
        obj1.save()
        
        
        return redirect('/forum/profile/?msg=ok') 
        #return render(request,'profile.html',{'updated':updated})
    form = UpdateProfile(instance=user)
    form1 = UpdateImage(instance=obj1)
    return render_to_response('update_profile.html',{ 'form':form, 'form1':form1},context_instance=RequestContext(request))   

@login_required  
def changepwd(request):
    #changed = " "
    #if request.POST:
     #   if 'changed' in request.GET:
      #      changed = request.GET['changed']
    return render(request,'changepwdform.html')
    
@login_required   
def changepassword(request):
    changed = " "
    user = auth.models.User.objects.get(username=request.user.username)
    opwd=request.POST['opwd']
    pwd=request.POST['npwd']
    if request.user.check_password(opwd):
        user.set_password(pwd)
        user.save()
        auth.login(request, auth.authenticate(username=request.user.username, password=pwd))
        #return HttpResponse("success")
        return redirect('/forum/profile/?changed=ok') 
    else:
        #return redirect('/forum/changepwd/?changed=wr')
        changed = "wrong"
        return render(request,'changepwdform.html',{'changed':changed})
        
        
       
        
def search_new(request):
    extra=[]
    query_string = ''
    found_entries = None
    if 'key' in request.GET:
        query_string = request.GET['key'].strip()
        entry_query = get_query(query_string, ['title'])
        found_entries = Question.objects.filter(entry_query).order_by('date_update')
        for i in found_entries :
                extra.append(UserProfile.objects.filter(user = i.user_id_id)) 
    return render_to_response('search.html',
            { 'query_string': query_string, 'found_entries': found_entries, 'extra':extra },
            context_instance=RequestContext(request)
        ) 
        
       

    
def home(request):
    
    question = Question.objects.aggregate(Max('id'))
    a = question['id__max']
    first = True
    read = []
    questlist = []
    ansextra = []    
    extra = []
    answerlist=[]
    read = []
    posted = ""
    if 'posted' in request.GET:
        posted = request.GET['posted']
        
    for i in range(a+100):
        if Question.objects.filter(id=(a-i)).exists():    
            q = Question.objects.get(id=(a-i))
        
            ans=Answer.objects.filter(question_id_id=q.id).aggregate(Max('id'))
            an = ans['id__max']
        
            if an == None :
                answerlist.append('Be the First one to Answer')
                status = 0
                read.append(status) 
            else:
                eas = Answer.objects.get(id=an)
       	        answerlist.append(eas)
       	        ansextra.append(UserProfile.objects.get(user_id = eas.user_id))
                status = 1
                read.append(status)
            questlist.append(q)
            extra.append(UserProfile.objects.get(user_id = q.user_id_id))
            
            final = zip(questlist,extra,answerlist,read,ansextra)
            paginator = Paginator(final, 5)

            try: page = int(request.GET.get("page", '1'))
            except ValueError: page = 1

            try:
               final = paginator.page(page)
            except (InvalidPage, EmptyPage):
               final = paginator.page(paginator.num_pages)
               
    return render(request,'home.html',{'posted':posted, 'final':final, 'first':first,'as':read,'ansextra':ansextra,'abc':answerlist})


@login_required
def display(request):
    return render(request,'post.html')
    

def question(request):
    
    if 'postt' in request.GET:
        quest = request.GET['postt']
        
        user_id= request.user.id
        user = User.objects.get(id = user_id)
        date_created = datetime.datetime.now()
        date_updated = datetime.datetime.now()
        obj = Question(title=quest,user_id=user,date_created=date_created,date_update=date_updated)
        obj.save()
        return HttpResponseRedirect("/forum/home/?posted=ok")

        
def writeans(request,ques_id):
    ques=[]
    extra=[]
    quest=Question.objects.get(id=ques_id)
    ques.append(UserProfile.objects.get(user = quest.user_id))
    
    anss = Answer.objects.filter(question_id_id=ques_id)
    for i in anss :
            extra.append(UserProfile.objects.get(user = i.user_id))
    return render(request,'ans.html',{'q':quest,'a':anss,'ques': ques,'extra':extra})
    

def answer(request,ques_id):
    ques = []
    extra=[]
    answered = False
    if request.method == "GET" and 'ans' in request.GET:
        answered = True
        answer = request.GET['answer']
        ques_obj=Question.objects.get(id=ques_id)
        user_id= request.user.id
      
        user = User.objects.get(id = user_id)
        obj = Answer(answer_text=answer,user_id=user,question_id_id=ques_id)
        obj.save()
        
        quest=Question.objects.get(id=ques_id)
        ques.append(UserProfile.objects.get(user = quest.user_id))
        anss = Answer.objects.filter(question_id_id=ques_id)
        for i in anss :
            extra.append(UserProfile.objects.get(user = i.user_id))
        return render(request,'ans.html',{'q':quest, 'a':anss,'extra':extra,'ques': ques,'answered':answered})
        

def recent_activity(request):
    deleted = " "   
    disp=" "
    l = []
    obj = User.objects.get(pk=request.user.id)
    if 'deleted' in request.GET:
        deleted = request.GET['deleted']
    if Question.objects.filter(user_id= obj.id).exists():
        q = Question.objects.filter(user_id= obj.id)
        l.append(q)
    else : 
        disp = " You have not posted any questions, yet ! "
    
    return render (request, 'recent_activity.html', { 'q':l, 'obj': obj,'disp':disp,'deleted':deleted})  
    
    

def delete_ques(request, ques_id):
    
    d = Question.objects.filter(user_id = request.user).get(pk=ques_id).delete()
    
    
    return HttpResponseRedirect("/forum/recent/?deleted=ok")
    

    
        


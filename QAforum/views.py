from django.shortcuts import render
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
# Create your views here.

#def register(request):
 #   return render(request,'reg.html')

#def main(request):
 #   return render(request,'main.html')
 

    
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
    username=request.user.username
    fname=request.user.first_name
    lname=request.user.last_name
    email=request.user.email
    obj = User.objects.get(username=request.user.username)
    obj1 = UserProfile.objects.get(user=obj)

    return render_to_response('profile.html', { 'username':username, 'fname':fname,'lname':lname,'email':email,'obj1':obj1})
    
    

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
        return HttpResponseRedirect('/forum/profile/') 
    form = UpdateProfile(instance=user)
    form1 = UpdateImage(instance=obj1)
    return render_to_response('update_profile.html',{ 'form':form, 'form1':form1},context_instance=RequestContext(request))   

@login_required  
def changepwd(request):
    return render(request,'changepwdform.html')
    
@login_required   
def changepassword(request):
    user = auth.models.User.objects.get(username=request.user.username)
    opwd=request.POST['opwd']
    pwd=request.POST['npwd']
    if request.user.check_password(opwd):
        user.set_password(pwd)
        user.save()
        auth.login(request, auth.authenticate(username=request.user.username, password=pwd))
        return HttpResponse("success")
    else:
        return HttpResponse("Enter correct password")
        
def search(request):
    error= False
    if 'key' in request.GET:
        title= request.GET['key'].strip()
        if not title:
            error= True
        else:
            obj = Question.objects.filter(title__icontains=title).order_by('date_update')
            return render(request, 'search.html', {'obj':obj,'title': title} )
    return render(request, 'search.html', {'error':error}
     )        

    
def home(request):
    
    question = Question.objects.aggregate(Max('id'))
    a = question['id__max']
    questlist = []
    extra = []
    for i in range(5):
        q = Question.objects.get(id=(a-i))
        extra.append(UserProfile.objects.get(user_id = q.user_id_id))
        questlist.append(q)
        final = zip(questlist,extra)
    return render(request,'home.html',{'final':final})

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
        
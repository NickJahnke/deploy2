from django.shortcuts import render,redirect
import bcrypt
from django.contrib import messages
from .models import User, Thought
from django.db.models.functions import Length

def index(request):
    return render(request, 'index.html')
#reg/login functions
def register(request):
    #if len(errors) > 0: ....
    #else:...
    errors = User.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/')
    else:
        password = request.POST['password']
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_pw,
            confirm_password = request.POST['confirm_password']
        )
        request.session['uuid'] = new_user.id
    return redirect('/thoughts')
def login(request):
    error = User.objects.login_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(error) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in error.items():
            messages.error(request, value)
        return redirect ('/')
    else:        
        #set user in session
        #redirect - /wishes
        list_of_user_emails = User.objects.filter(email = request.POST['login_email'])
        request.session['uuid'] = list_of_user_emails[0].id 
    return redirect('/thoughts')
def logout(request):
    request.session.flush()
    return redirect('/')

#renders
def show_thoughts(request):
    if 'uuid' not in request.session:
        return redirect('/')
    
    context = {
        'user': User.objects.get(id = request.session['uuid']),
        'thoughts': Thought.objects.all().order_by(Length('users_who_like').asc()),
        
    }
    return render(request,'dashboard.html',context)
def show_details(request,thought_id):
    if 'uuid' not in request.session:
        return redirect('/')
    thought_instance = Thought.objects.get(id = thought_id)
    context = {
        'thought':thought_instance,
        'users': User.objects.filter(liked_thoughts=thought_id),
        'logged_user': User.objects.get(id = request.session['uuid']),
        
    }
    return render(request,'details.html',context)

#redirects
def create_thought(request):
    errors = Thought.objects.new_thought_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/thoughts')
    else:
        user = User.objects.get(id = request.session['uuid'])
        new_thought = Thought.objects.create(
            description = request.POST['new_desc'],
            uploaded_by = user
        )
    return redirect('/thoughts')

def like_thought(request,thought_id):
    logged_user = User.objects.get(id=request.session['uuid'])
    liked_thought = Thought.objects.get(id=thought_id)
    liked_thought.users_who_like.add(logged_user)
    return redirect(f'/thoughts/{thought_id}')
def unlike_thought(request,thought_id):
    logged_user = User.objects.get(id=request.session['uuid'])
    liked_thought = Thought.objects.get(id=thought_id)
    liked_thought.users_who_like.remove(logged_user)
    return redirect(f'/thoughts/{thought_id}')
def remove_thought(request,thought_id):
    thought_instance = Thought.objects.get(id=thought_id)
    thought_instance.delete()
    return redirect('/thoughts')
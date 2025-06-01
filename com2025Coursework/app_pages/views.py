from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, UserSignUpForm, AlbumForm, CommentForm, RecommendForm, ContactsForm
from app_album_viewer.models import Album, Song, Comment, UserDetails
import re, os
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail


# Create your views here.
def home(request): # This is the home page for the website
    image_url = '/media/dripping-stereo.png'
    return render(request, 'base.html', {'image_url': image_url})

def contact(request): # This shows the contact 
    form = ContactsForm()
    image_url = '/media/dripping-stereo.png'
    if request.method == 'POST':
        form = ContactsForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            email_verification = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_verification, email):
                error_message = "Email is invalid"
                return render(request, 'contact.html', {'form': form, 'image_url': image_url, 'error_message': error_message})
            form = ContactsForm()
            subject = "User Query"
            send_mail(subject, message, email, [settings.DEFAULT_FROM_EMAIL])
            success_message = "Email successfully sent"
            return render(request, 'contact.html', {'form': form, 'image_url': image_url, 'success_message': success_message})
            
            
    return render(request, 'contact.html', {'form': form, 'image_url': image_url})

def login(request): #This view autheticates the user and allows them to login
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            # Attempt to authenticate against UserDetails
            if user is not None:
                auth_login(request, user)
                request.session['username'] = username
                return redirect('/album/welcome')
        else:
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if user_login(request, username_or_email, password) == False:
                form = LoginForm()
                image_url = '/media/dripping-stereo.png' # This allows the use of an image
                error_message = "Invalid username or password. Please try again."
                return render(request, 'login.html', {'form': form, 'image_url': image_url, 'error_message': error_message})
            else:
                try:
                    user = UserDetails.objects.get(email=username_or_email)
                    stored_username = user.username
                    request.session['username'] = stored_username
                    return redirect('/album/welcome')
                except UserDetails.DoesNotExist:
                    request.session['username'] = username_or_email
                    return redirect('/album/welcome')
            
    form = LoginForm()
    image_url = '/media/dripping-stereo.png'
    return render(request, 'login.html', {'form': form, 'image_url': image_url})

def user_login(request, email_username, password): #This allows the non superuser to login
    try:
        user = UserDetails.objects.get(username=email_username)
        stored_password = user.password 
        password_matched = check_password(password, stored_password)
        if password_matched:
            return True 
        else:
            return False 
    except UserDetails.DoesNotExist:
        pass
    
    try:
        user = UserDetails.objects.get(email=email_username)
        stored_password = user.password  
        password_matched = check_password(password, stored_password)
        if password_matched:
            return True
        else:
            return False 

    except UserDetails.DoesNotExist:
        pass

    return False


def signup(request): #This is the user sign up page
    form = UserSignUpForm()
    image_url = '/media/dripping-stereo.png'

    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            email_verification = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            fullname = form.cleaned_data['fullname']

            # Split full name into first and last name
            name_parts = fullname.split()
            if len(name_parts) < 2:
                form.add_error('fullname', "Invalid fullname, enter your first name and last name")
                return render(request, 'signup.html', {'form': form, 'image_url': image_url})
            if not re.match(email_verification, email):
                error_message = "Invalid email"
                return render(request, 'signup.html', {'form': form, 'image_url': image_url, 'error_message': error_message})

            if len(username) < 5:
                error_message = "Username is too short"
                return render(request, 'signup.html', {'form': form, 'image_url': image_url, 'error_message': error_message})

            if password != form.cleaned_data['password1']:
                error_message = "Passwords do not match"
                return render(request, 'signup.html', {'form': form, 'image_url': image_url, 'error_message': error_message})

            if len(password) < 6:
                error_message = "Passwords is too short"
                return render(request, 'signup.html', {'form': form, 'image_url': image_url, 'error_message': error_message})
            
            if UserDetails.objects.filter(username=username).exists():
                error_message = "Username is already used"
                return render(request, 'signup.html', {'form': form, 'image_url': image_url, 'error_message': error_message})

            if UserDetails.objects.filter(email=email).exists():
                error_message = "Email is already used"
                return render(request, 'signup.html', {'form': form, 'image_url': image_url, 'error_message': error_message})
                
                


            first_name, last_name = name_parts[0], ' '.join(name_parts[1:])

            new_user = UserDetails(
                firstname=first_name,
                surname=last_name,
                email=email,
                username=username,
                password=make_password(password)
            )
            new_user.save()

            request.session['username'] = username 
            return redirect('/album/welcome', {'image_url': image_url, 'username': username, 'form': form})

    return render(request, 'signup.html', {'form': form, 'image_url': image_url})

def about(request): #This is the about page for the website
    image_url = '/media/dripping-stereo.png'
    return render(request, 'aboutus.html', {'image_url': image_url})






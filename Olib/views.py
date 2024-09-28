from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model,logout
from django.contrib.auth.decorators import login_required
from Olib.forms import Login_Form, Signup_Form, UserProfileForm
from .models import user_collection  # Assuming this is your custom model for user profiles
import logging
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

# Create your views here.


# Set up logger
logger = logging.getLogger(__name__)

@login_required
def index(request):
    return render(request,"index.html");

def sign_up(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('fullname')
        password = request.POST.get('password')
        email= request.POST.get('email')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, "Username Already taken")
            return redirect('/signup')

        user = User.objects.create(
            username = username,
            first_name = first_name,
            email = email,
        )
        user.set_password(password)
        user.save()
        messages.info(request, "Your account has been created")
        return redirect('/login')
        # messages.success(request, f'Your account has been created ! You are now able to log in')
        # signup = Sign_up(username=username, email=email, password = password)
        # signup.save()
    return render(request,"sign-up.html")

def log_in(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request, "Invalid Username or password")
            return redirect('/login')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.info(request, "Invalid Credentials")
            return redirect('/login')

        else:
            login(request, user)
            messages.info(request, "Logged in Successfully")
            return redirect('/home')  # Redirect to profile view after successful login
    return render(request, "sign-in.html")

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    storage = messages.get_messages(request)
    storage.used = True  # Mark messages as used so they won't appear again
    return HttpResponse("<strong>You are logged out.</strong> <a href='login'>login</a>")

def forgot_password(request):
    # user = User
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            messages.info(request, "Username is not valid")
        u = User.objects.get(username=username)
        u.set_password(password)
        u.save()
        return redirect('/login')
    return render(request,"forgot-password.html")

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        # Retrieve updated data from the form
        full_name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')

        # Update user fields
        user.first_name = full_name
        user.username = username
        user.email = email
        user.save()

        return redirect('profile')
    test = {
        "user_id": request.session.session_key,  # Store session key as user ID
        "name": user.first_name,
        "username": user.username,
        "email" :user.email,
    }

    user_collection.update_one(
        {"user_id": request.session.session_key},  # Find the document by session key
        {"$set": test},  # Update the document with the new data
        upsert=True  # Insert a new document if it doesn't exist
    )


    return render(request, 'myaccount.html',{'user': user})


def getAllUser(request):
    users = list(user_collection.find())
    users_list = "<br>".join([f"{user['name']} - {user['username']} - {user['email']}" for user in users])  # Format users for display
    return HttpResponse(users_list)

def view_book(request):

    return render(request,"book-overview.html")


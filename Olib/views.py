from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages , sessions
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model,logout
from django.contrib.auth.decorators import login_required
from Olib.forms import Login_Form, Signup_Form ,UserProfileForm
from .models import user_collection
import logging

# Create your views here.


# Set up logger
logger = logging.getLogger(__name__)


def index(request):

    return render(request,"index.html");

def sign_up(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('fullname')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, "Username Already taken")
            return redirect('/signup')

        user = User.objects.create(
            username = username,
            first_name = first_name,
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

        # Session create
        request.session['name'] = username
        # request.session.set_expiry(20)

        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request, "Invalid Username or password")
            return redirect('/login')



        user = authenticate(request,username=username,password=password)

        if user is None:
            messages.info(request, "Invalid")
            return redirect('/login')

        else:
            login(request,user)
            messages.info(request, "log in Succusfully")
            # return redirect('/home')
    return render(request , "sign-in.html")

def user_logout(request):
   logout(request)
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


def profile(request):
    user_id = request.session.get('user_id')

    if user_id:
        # Fetch user data from MongoDB using the session's user ID
        user_data = user_collection.find_one({"user_id": user_id})

        if user_data:
            return render(request, 'myaccount.html', {'user': user_data})  # Display stored data

    # If the user is visiting for the first time or doesn't exist in MongoDB
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = {
                "user_id": request.session.session_key,  # Store session key as user ID
                "name": request.POST.get('name'),
                "username": request.POST.get('username'),
                "email": request.POST.get('email'),
                "phone": request.POST.get('phone'),
                "photo": request.POST.get('photo')
            }

            print(user_profile)

            try:
                user_collection.insert_one(user_profile)  # Save the data to MongoDB
                # Save the user ID in the session
                messages.success(request, ('Your Profile Is Updated.'))
                request.session['user_id'] = request.session.session_key
                return redirect('home')
            except Exception as e:
                logger.error(f"Error occurred while inserting data into MongoDB: {e}")
                return HttpResponse("<h3>Error occurred while saving data.</h3>")


    else:
        form = UserProfileForm()

    return render(request, 'myaccount.html', {'form': form})


def getAllUser(request):
    users = list(user_collection.find())
    users_list = "<br>".join([f"{user['name']} - {user['username']} - {user['email']}" for user in users])  # Format users for display
    return HttpResponse(users_list)

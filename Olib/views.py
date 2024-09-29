from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model,logout
from django.contrib.auth.decorators import login_required
from Olib.forms import Login_Form, Signup_Form, UserProfileForm
from .models import *
from .forms import CategoryForm
import logging
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.db.models import Max
from django.core.files.storage import FileSystemStorage
from pymongo import MongoClient
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# Set up logger
logger = logging.getLogger(__name__)

@login_required
def index(request):
    return render(request,"index.html")

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
            UserProfile.objects.get_or_create(user=user)

            # Redirect to user_choice if they haven't submitted interests yet
            user_profile = UserProfile.objects.get(user=user)
            if not user_profile.has_submitted_interests:
                return redirect('/interest')
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


# def getAllUser(request):
#     users = list(user_collection.find())
#     users_list = "<br>".join([f"{user['name']} - {user['username']} - {user['email']}" for user in users])  # Format users for display
#     return HttpResponse(users_list)

def view_book(request):

    return render(request,"book-overview.html")

def user_choice(request):
    user = request.user

    # Check if the user has already submitted their interests
    user_profile = UserProfile.objects.get(user=user)

    if user_profile.has_submitted_interests:
        return redirect('/home')  # Redirect to home if already submitted

    if request.method == "POST":
        interests = request.POST.getlist('c')

        test = {
            "username": user.username,
            "interest": interests,
        }
        user_interest.insert_one(test)

        # Update the user profile to mark that interests have been submitted
        user_profile.has_submitted_interests = True
        user_profile.save()

        return redirect('/home')  # Redirect after saving interests

    return render(request, "interest.html")


def admin_index(request):
    max_user_id = User.objects.aggregate(Max('id'))['id__max']

    return render(request,"Admin-index.html",{'max_user_id': max_user_id})

def booklist(request):
    return render(request,"booklist.html")

@csrf_exempt
def add_book(request):
    if request.method == 'POST':
        # Retrieve form data
        book_name = request.POST['BookName']
        author_name = request.POST['AuthorName']
        publisher_name = request.POST['PublisherName']
        publication_date = request.POST['date']
        categories = request.POST['Categories']
        description = request.POST['Description']

        # Handle file uploads
        cover_image = request.FILES['CoverImage']
        book_pdf = request.FILES['BookPDF']

        # Save files to the media directory
        fs = FileSystemStorage()
        cover_image_path = fs.save(cover_image.name, cover_image)
        book_pdf_path = fs.save(book_pdf.name, book_pdf)

        # Format the date
        try:
            publication_date = datetime.strptime(publication_date, '%Y-%m-%d')
        except ValueError:
            return render(request, 'addbook.html', {'error': 'Invalid date format'})

        # Store book details in MongoDB
        new_book = {
            'book_name': book_name,
            'author_name': author_name,
            'publisher_name': publisher_name,
            'publication_date': publication_date,
            'categories': categories,
            'description': description,
            'cover_image': cover_image_path,
            'book_pdf': book_pdf_path,
        }

        # Insert the new book record into MongoDB
        user_book.insert_one(new_book)

        # Redirect to a success page or display a success message
        return HttpResponse("<h2>success_page</h2>")

    return render(request, "addbook.html")

def book_category(request):

    return render(request,"booklist.html")

def get_all(request):
    return render(request,"userlist.html")

def upload_pdf(request):
    return render(request,"addbook.html")

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = request.POST.get('category_name')
            # Assuming you are using a MongoDB model
            CategoryForm.objects.update_one(
                {},
                {'$addToSet': {'selected_categories': category_name}}  # Use $addToSet to avoid duplicates
            )
            return redirect('categories')  # Redirect after successful submission
    else:
        form = CategoryForm()

    return render(request, "addcategory.html", {'form': form})

def add_user(request):
    return render(request,"adduser.html")

def categorylist(request):
    return render(request,"Categorylist.html")


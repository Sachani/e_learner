from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def admin_index(request):
    return render(request,"Admin-index.html")

def booklist(request):
    return render(request,"booklist.html")

def add_book(request):
    return render(request,"addbook.html")

def book_category(request):
    return render(request,"booklist.html")

def get_all(request):
    return render(request,"userlist.html")

def upload_pdf(request):
    return render(request,"addbook.html")

def add_category(request):
    return render(request,"addcategory.html")

def add_user(request):
    return render(request,"adduser.html")

def categorylist(request):
    return render(request,"Catogerylist.html")

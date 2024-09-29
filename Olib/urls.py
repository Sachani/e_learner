from django.contrib import admin
from django.urls import path
from Olib import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path("signup",views.sign_up,name="Sign_up"),
   path("interest", views.user_choice, name="Interest"),
   path("login",views.log_in,name="Login"),
   path("logout",views.user_logout,name="logout"),
   path("forgot",views.forgot_password,name="forgot_password"),
   path("",views.index,name="Home"),
   path("home",views.index,name="Home"),
   path("view_book",views.view_book,name="Book"),
   path("profile",views.profile,name="Profile"),

   # admin
   path("host",views.admin_index,name="Admin-Home"),
   path("list_book",views.booklist,name="Books"),
   path("add_book",views.add_book,name="Add_Book"),
   path("bookByCategory",views.book_category,name="BookByCategory"),
   path("get_users",views.get_all,name="All_Users"),
   path("upload_pdf",views.upload_pdf,name="Upload"),
   path("add_category",views.add_category,name="Add_Category"),
   path("categories",views.categorylist,name="Category"),
   path("add_user",views.add_user,name="Add_User"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import path
from Olib import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path("signup",views.sign_up,name="Sign_up"),
   path("login",views.log_in,name="Login"),
   path("logout",views.user_logout,name="logout"),
   path("forgot",views.forgot_password,name="forgot_password"),
   path("",views.index,name="Home"),
   path("home",views.index,name="Home"),
   path("view_book",views.view_book,name="Home"),
   path("profile",views.profile,name="Profile"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
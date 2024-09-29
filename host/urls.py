from django.contrib import admin
from django.urls import path
from Olib import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",views.admin_index,name="Home"),
    path("home",views.admin_index,name="Home"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
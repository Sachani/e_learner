from django.contrib import admin
from django.urls import path
from host import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",views.admin_index,name="Home"),
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
from django.db import models
from .db_connections import db
from django.contrib.auth.models import User

from .views import categorylist

user_collection = db['User_Collection']
user_interest = db['User_Interest']
user_book = db['User_Book']
categorylist = db['categories']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_submitted_interests = models.BooleanField(default=False)










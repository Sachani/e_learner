# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import user_collection

# from .models import UserProfile

class Signup_Form(UserCreationForm):
    

    class Meta:
        model = User
        fields = ['username' , 'password']
        widgets = {
           'username': forms.TextInput(attrs={'class': 'form-control'}),
           'first_name': forms.TextInput(attrs={'class': 'form-control'}),
           'password': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

class Login_Form(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username' : forms.TextInput(attrs={'class' : 'form-control'}),
            'password' : forms.TextInput(attrs={'class' : 'form-control'}),
        }

class UserProfileForm(forms.Form):
    user_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))





from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

CLASS_INPUT = "px-3 py-2 rounded-xl w-full border-black border"

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  
     
    username = forms.CharField(widget=forms.TextInput(attrs={
        "id":"username",
        "placeholder":"Enter username...",
        "class":CLASS_INPUT
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "id":"email",
        "placeholder":"Email adress",
        "class":CLASS_INPUT
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "id":"password1",
        "placeholder":"Password",
        "class":CLASS_INPUT
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "id":"password2",
        "placeholder":"Confirm Password",
        "class":CLASS_INPUT
    }))

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password'] 
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        "id":"username",
        "placeholder":"Enter username...",
        "class":CLASS_INPUT
    }))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "id":"password",
        "placeholder":"password...",
        "class":CLASS_INPUT
    }))
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth.models import User
from typing import Any 
from django import forms
from django.forms.widgets import PasswordInput,TextInput


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    #Unique Email Restriction


    def __init__(self, *args, **kwargs):
        super(CreateUserForm,self).__init__(*args, **kwargs)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        # if email is used before. That raise text as "This email is Invalid"
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This Email is Invalid')
        
        if len(email) >= 350:
            raise forms.ValidationError('Your Email is too Long')
    
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget = TextInput)
    password = forms.CharField(widget = PasswordInput())


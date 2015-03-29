from django import forms
from models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    cpassword = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password')
        
    def clean_cpassword(self):
        password = self.cleaned_data.get("password")
        cpassword = self.cleaned_data.get("cpassword")
        if not cpassword:
            raise forms.ValidationError("You must confirm your password")
        
        if password != cpassword:
            raise forms.ValidationError("Passwords don't match")
        return cpassword
        
        
        
class LoginForm(forms.ModelForm):

    password = forms.CharField(label=("Password"), widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')
        
 
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
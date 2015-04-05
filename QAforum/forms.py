from django import forms
from models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'reg_fname', 'placeholder': 'First Name'}), max_length=20, label='')    
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'reg_lname', 'placeholder': 'Last Name'}), max_length=20, label='')
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'reg_uname', 'placeholder': 'User Name'}), max_length=20, label='')
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'reg_mail', 'placeholder': 'Email'}), max_length=20, label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'reg_pwd', 'placeholder': 'Your password...'}), max_length=20, label='')
    cpassword = forms.CharField(widget=forms.PasswordInput(attrs={'class':'reg_pwd', 'placeholder': 'Re-enter your password'}), max_length=20, label='')
    
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

    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'youpasswd', 'placeholder': ''}), max_length=20, label='password')

    class Meta:
        model = User
        fields = ('username', 'password')
        
 
        
class UserProfileForm(forms.ModelForm):

    website = forms.CharField(widget=forms.TextInput(attrs={'class':'reg_website', 'placeholder': 'Website'}), max_length=20, label='')
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

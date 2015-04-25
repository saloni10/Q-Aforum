from django import forms
from models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError 
from views import *
from django.core.validators import RegexValidator


class UserForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'reg_fname', 'placeholder': 'First Name'}), max_length=50, label='',validators=[
        RegexValidator(
            regex='^[a-zA-Z]*$',
            message='First Name can not be Numeric',
            code='invalid_firstname'
        ),
    ])    
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'reg_lname', 'placeholder': 'Last Name'}), max_length=50, label='',validators=[
        RegexValidator(
            regex='^[a-zA-Z]*$',
            message='Last Name can not be Numeric',
            code='invalid_lastname'
        ),
     ])
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'reg_uname', 'placeholder': 'User Name'}), max_length=50, label='')
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'reg_mail', 'placeholder': 'Email'}), max_length=50, label='')
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

    website = forms.URLField(widget=forms.TextInput(attrs={'class':'reg_website', 'placeholder': 'Website'}), max_length=50, label='')
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')



class UpdateProfile(forms.ModelForm):
    username = forms.CharField(initial = "profile.user.username")
    email = forms.EmailField(initial = "profile.user.email")
    first_name = forms.CharField(initial = "profile.user.username")
    last_name = forms.CharField(initial = "profile.user.username")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    """def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user"""
        
class UpdateImage(forms.ModelForm):
    website = forms.URLField(initial = "https://www.google.com")
    #picture = forms.ImageField(ModelMultipleChoiceField(queryset=Author.objects.all()))
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')


#class AnswerForm(forms.ModelForm):
 #   answer_text = forms.CharField(widget=forms.Textarea(attrs={'class':'ans_text', 'placeholder': 'Your Answer.....'}), max_length=1000, label='') 
  #  class Meta:
   #     model = Answer
    #    fields = ('answer_text' ,)
    

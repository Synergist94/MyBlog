from users.models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(label='Никнейм', required=False, widget=forms.TextInput(attrs={'class': 'form_input'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ImagesUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', required=False, widget=forms.TextInput(attrs={'class': 'form_input'}))
    password1 = forms.CharField(label='Пароль', required=False, widget=forms.PasswordInput(attrs={'class': 'form_input'}))
    password2 = forms.CharField(label='Павтор пароля', required=False, widget=forms.PasswordInput(attrs={'class': 'form_input'}))
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', required=False, widget=forms.TextInput(attrs={'class': 'form_input'}))
    password = forms.CharField(label='Пароль', required=False, widget=forms.PasswordInput(attrs={'class': 'form_input'}))

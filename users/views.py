from django.shortcuts import render,redirect
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main.forms import *
from users.forms import RegisterUserForm, LoginUserForm,ImagesUpdateForm,ProfileUpdateForm
from main.utils import *
from users.models import Profile
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView,UpdateView,DetailView

class AllUser(DataMixin, ListView):
    model = User
    template_name = 'users/allusers.html'
    context_object_name = 'allusers'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Все пользователи на сайте')
        return dict(list(context.items()) + list(c_def.items()))

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    context_object_name = 'user'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация на сайте')
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile', user.id)
    
class UserLogin(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    
    def get_success_url(self):
        return reverse_lazy('home')
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Страница авторизации')
        return dict(list(context.items()) + list(c_def.items()))

def Logout_user(request):
    logout(request)
    return redirect('home')
    
class UserProfile(LoginRequiredMixin, DataMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'alluser'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Моя страница')
        return dict(list(context.items()) + list(c_def.items()))

class ImageUpdate(LoginRequiredMixin, DataMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'users/u_settings.html'
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = User.objects.get(id=self.kwargs['pk'])
        instance.save()
        return redirect('profile', instance.user.id)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Страница редактирования профиля')
        return dict(list(context.items()) + list(c_def.items()))
from django.shortcuts import render,redirect
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main.forms import *
from users.forms import MessageForm, RegisterUserForm, LoginUserForm,ImagesUpdateForm,ProfileUpdateForm
from main.utils import *
from users.models import Profile, Chat
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView,UpdateView,DetailView

class DialogsView(ListView):
    def get(self, request):
        chats = Chat.objects.filter(members__in=[request.user.id])
        return render(request, 'users/dialogs.html', {'user_profile':request.user, 'chats': chats})

class MessagesView(ListView):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None
 
        return render(request, 'users/messages.html',{'user_profile': request.user, 'chat': chat, 'form': MessageForm()})
 
    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('users:messages', kwargs={'chat_id': chat_id}))

class CreateDialogView(ListView):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        return redirect(reverse('users:messages', kwargs={'chat_id': chat.id}))

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
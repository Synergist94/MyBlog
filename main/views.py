from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .utils import *
from main.forms import AddMainBlogForm,UpdateMainBlogForm
from main.models import MainBlog

class UserPostListView(DataMixin,ListView):
    model = MainBlog
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return MainBlog.objects.filter(author=user)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Страница удаления новости')
        return dict(list(context.items()) + list(c_def.items()))

class Main_blog_delete(LoginRequiredMixin, DataMixin, DeleteView):
    model = MainBlog
    template_name = 'blog/blog_delete.html'
    success_url = reverse_lazy('home')
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Страница удаления новости')
        return dict(list(context.items()) + list(c_def.items()))

class Main_blog_Update(LoginRequiredMixin, DataMixin, UpdateView):
    form_class = UpdateMainBlogForm
    model = MainBlog
    slug_field = 'id'
    template_name = 'blog/blog_update.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Страница добавления новой записи')
        return dict(list(context.items()) + list(c_def.items()))

class Main_blog_Add(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddMainBlogForm
    template_name = 'blog/blog_add.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Страница добавления новой записи')
        return dict(list(context.items()) + list(c_def.items()))
    

class Main_blogListView(DataMixin, ListView):
    model = MainBlog
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Python bytes blog')
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_queryset(self):
        return MainBlog.objects.filter(status=1)
    
class Main_blogDetail(DataMixin, DetailView):
    model = MainBlog
    template_name = 'blog/post_detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Python bytes blog')
        return dict(list(context.items()) + list(c_def.items()))

class Category(DataMixin, ListView):
    model = MainBlog
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Python bytes blog')
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_queryset(self):
        return MainBlog.objects.filter(category__slug=self.kwargs['slug'],status=1)
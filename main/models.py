from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from tinymce.models import HTMLField
from tinymce import models as tinymce_models

STATUS = (
    (0,"Нет"),
    (1,"Да")
)

class MainBlog(models.Model):
    title = models.CharField('Название новости', max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True,verbose_name='Адрес новости на англиском')
    text = tinymce_models.HTMLField('Краткое описание новости')
    full_text = tinymce_models.HTMLField('Полное описание новости',blank=True)
    author = models.ForeignKey(User,on_delete= models.PROTECT,related_name='main_blog')
    category = models.ForeignKey('Category', on_delete= models.PROTECT,verbose_name='Категория',related_name='main_blog_category')
    created_on = models.DateTimeField('Дата публикации', auto_now_add=True)
    status = models.IntegerField('Опубликован?',choices=STATUS, default=1)

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        
    def get_absolute_url(self):
        return reverse('blog', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
    
class Category(models.Model):
    title = models.CharField('Название категории', max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    post = models.ForeignKey('MainBlog', on_delete=models.PROTECT, related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
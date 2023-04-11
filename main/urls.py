from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Main_blogListView.as_view(), name='home'),
    path('user/<str:username>/', views.UserPostListView.as_view(), name='user_posts'),
    path('blog/<slug:slug>/', views.Main_blogDetail.as_view(), name='post_detail'),
    path('blog_add/', views.Main_blog_Add.as_view(), name='blog_add'),
    path('blog/<int:pk>/update/', views.Main_blog_Update.as_view(), name='blog_update'),
    path('blog/<int:pk>/delete/', views.Main_blog_delete.as_view(), name='blog_delete'),
    path('category/<slug:slug>/', views.Category.as_view(), name='post_category'),
    
]

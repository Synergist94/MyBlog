from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users.views import RegisterUser,UserProfile,Logout_user,UserLogin,ImageUpdate,AllUser

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('main.urls')),
    path('registration/', RegisterUser.as_view(), name='register'),
    path('allusers/', AllUser.as_view(), name='allusers'),
    path('profile/<int:pk>/', UserProfile.as_view(), name='profile'),
    path('profile/<int:pk>/settings/', ImageUpdate.as_view(), name='u_settings'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', Logout_user, name='logout'),
    path('tinymce/', include('tinymce.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
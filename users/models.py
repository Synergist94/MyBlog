from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False)
    image = models.ImageField(default='default.png', upload_to='profile_pics', blank=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            
    def get_absolute_url(self):
        return reverse('Profile', kwargs={'pk': self.pk})
            
    class Meta:
        verbose_name = 'Аккаунты'
        verbose_name_plural = 'Аккаунты'

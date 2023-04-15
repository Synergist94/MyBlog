from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from PIL import Image

class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, _('Dialog')),
        (CHAT, _('Chat'))
    )
 
    type = models.CharField(
        _('Тип'),
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(User, verbose_name=_("Участник"))
 
    
    def get_absolute_url(self):
        return 'users:messages', (), {'chat_id': self.pk }
 
 
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, verbose_name=_("Чат"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    message = models.TextField(_("Сообщение"))
    pub_date = models.DateTimeField(_('Дата сообщения'), default=timezone.now)
    is_readed = models.BooleanField(_('Прочитано'), default=False)
 
    class Meta:
        ordering=['pub_date']
 
    def __str__(self):
        return self.message

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

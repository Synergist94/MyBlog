from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Profile

@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ('id','user', 'get_html_image')
    list_display_links = ('id','user')
    fields = ('user', 'image', 'get_html_image')
    readonly_fields = ('get_html_image',)
    
    def get_html_image(self, object):
        return mark_safe(f"<img src='{object.image.url}' width=50>")
    
    get_html_image.short_description = "Миниатюра"

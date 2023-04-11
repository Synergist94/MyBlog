from django.contrib import admin
from .models import MainBlog, Category

@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ('id','title',)

@admin.register(MainBlog)
class MainBlog(admin.ModelAdmin):
    list_display = ('id','title','category','created_on','author','status')
    list_display_links = ('id','title',)
    list_filter = ('author','created_on','title',)
    search_fields = ['title', 'content']
    save_on_top = True
    actions = ['publish', 'unpublish']

    def publish(self, request, queryset):
        row_update = queryset.update(status=1)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')
    
    def unpublish(self, request, queryset):
        row_update = queryset.update(status=0)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change',)

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)

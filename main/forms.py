from django import forms
from django.core.exceptions import ValidationError
from tinymce.widgets import TinyMCE
from main.models import *

class UpdateMainBlogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"

    class Meta:
        model = MainBlog
        fields = ['title', 'slug', 'text', 'full_text', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'slug': forms.TextInput(attrs={'class': 'input'}),
            'text': TinyMCE(attrs={'class': 'textarea2'}),
            'full_text': forms.Textarea(attrs={'class': 'textarea2'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return title

class AddMainBlogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"

    class Meta:
        model = MainBlog
        fields = ['title', 'slug', 'text', 'full_text', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'slug': forms.TextInput(attrs={'class': 'input'}),
            'text': TinyMCE(attrs={'class': 'textarea2'}),
            'full_text': forms.Textarea(attrs={'class': 'textarea2'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return title

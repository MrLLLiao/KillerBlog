from django import forms
from django.utils.text import slugify

from .models import BlogSetting, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'excerpt', 'content', 'cover_image', 'category', 'tags', 'status', 'allow_comment']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input', 'placeholder': '文章标题'}),
            'slug': forms.TextInput(attrs={'class': 'input', 'placeholder': '自动生成或自定义'}),
            'excerpt': forms.Textarea(attrs={'class': 'textarea', 'rows': 2, 'placeholder': '一句话概括'}),
            'content': forms.Textarea(attrs={'class': 'textarea', 'rows': 10, 'placeholder': '支持 Markdown 撰写'}),
            'category': forms.Select(attrs={'class': 'select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'select'}),
            'status': forms.Select(attrs={'class': 'select'}),
            'allow_comment': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        title = self.cleaned_data.get('title')
        if not slug and title:
            slug = slugify(title)
        return slug


class BlogSettingForm(forms.ModelForm):
    class Meta:
        model = BlogSetting
        fields = ['title', 'subtitle', 'description', 'hero_image', 'theme']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'subtitle': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'textarea', 'rows': 4}),
            'theme': forms.Select(attrs={'class': 'select'}),
        }

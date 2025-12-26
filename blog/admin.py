from django.contrib import admin

from .models import BlogSetting, Category, Post, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'views')
    search_fields = ('title', 'content')
    list_filter = ('status', 'category', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('author', 'category', 'tags')


@admin.register(BlogSetting)
class BlogSettingAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'theme', 'updated_at')

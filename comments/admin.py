from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'is_approved', 'likes', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('content', 'author__username')
    autocomplete_fields = ('post', 'author', 'parent')

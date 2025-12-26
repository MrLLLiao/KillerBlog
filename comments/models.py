from django.conf import settings
from django.db import models
from blog.models import Post


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField('内容')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_approved = models.BooleanField('审核通过', default=True)
    likes = models.PositiveIntegerField('点赞数', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def __str__(self):
        return f"{self.author} - {self.content[:20]}"

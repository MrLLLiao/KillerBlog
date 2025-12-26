from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField('分类', max_length=50, unique=True)
    slug = models.SlugField('标识', max_length=60, unique=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('标签', max_length=50, unique=True)
    slug = models.SlugField('标识', max_length=60, unique=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class Post(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, '草稿'),
        (PUBLISHED, '已发布'),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('标识', max_length=220, unique=True)
    excerpt = models.CharField('摘要', max_length=220, blank=True)
    content = models.TextField('内容')
    cover_image = models.ImageField('封面图', upload_to='posts/covers/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default=DRAFT)
    allow_comment = models.BooleanField('允许评论', default=True)
    views = models.PositiveIntegerField('浏览数', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:post-detail', kwargs={'slug': self.slug})


class BlogSetting(models.Model):
    THEME_CHOICES = (
        ('light', '简洁亮色'),
        ('dark', '经典暗色'),
    )

    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_setting')
    title = models.CharField('博客标题', max_length=120, default='ABlog')
    subtitle = models.CharField('博客副标题', max_length=180, blank=True)
    description = models.TextField('描述', blank=True)
    hero_image = models.ImageField('背景图', upload_to='settings/', blank=True, null=True)
    theme = models.CharField('主题', max_length=20, choices=THEME_CHOICES, default='light')
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '博客设置'
        verbose_name_plural = '博客设置'

    def __str__(self):
        return f"{self.owner}'s settings"

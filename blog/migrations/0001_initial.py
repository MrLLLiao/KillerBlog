from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='分类')),
                ('slug', models.SlugField(max_length=60, unique=True, verbose_name='标识')),
            ],
            options={'verbose_name': '分类', 'verbose_name_plural': '分类'},
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='标签')),
                ('slug', models.SlugField(max_length=60, unique=True, verbose_name='标识')),
            ],
            options={'verbose_name': '标签', 'verbose_name_plural': '标签'},
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('slug', models.SlugField(max_length=220, unique=True, verbose_name='标识')),
                ('excerpt', models.CharField(blank=True, max_length=220, verbose_name='摘要')),
                ('content', models.TextField(verbose_name='内容')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='posts/covers/', verbose_name='封面图')),
                ('status', models.CharField(choices=[('draft', '草稿'), ('published', '已发布')], default='draft', max_length=10, verbose_name='状态')),
                ('allow_comment', models.BooleanField(default=True, verbose_name='允许评论')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='浏览数')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='blog.category')),
                ('tags', models.ManyToManyField(blank=True, related_name='posts', to='blog.tag')),
            ],
            options={'verbose_name': '文章', 'verbose_name_plural': '文章', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='BlogSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='ABlog', max_length=120, verbose_name='博客标题')),
                ('subtitle', models.CharField(blank=True, max_length=180, verbose_name='博客副标题')),
                ('description', models.TextField(blank=True, verbose_name='描述')),
                ('hero_image', models.ImageField(blank=True, null=True, upload_to='settings/', verbose_name='背景图')),
                ('theme', models.CharField(choices=[('light', '简洁亮色'), ('dark', '经典暗色')], default='light', max_length=20, verbose_name='主题')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='blog_setting', to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': '博客设置', 'verbose_name_plural': '博客设置'},
        ),
    ]

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import DetailView, ListView
from rest_framework import viewsets, permissions
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


from .forms import PostForm, BlogSettingForm
from .models import Category, Tag, Post, BlogSetting
from .serializers import CategorySerializer, TagSerializer, PostSerializer, BlogSettingSerializer

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from .models import Post, BlogSetting


class UserBlogView(ListView):
    model = Post
    template_name = "blog/user_blog.html"
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        User = get_user_model()
        self.blog_owner = get_object_or_404(User, username=kwargs["username"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = (
            Post.objects.filter(author=self.blog_owner)
            .select_related("author", "category")
            .prefetch_related("tags")
        )
        if self.request.user != self.blog_owner:
            qs = qs.filter(status=Post.PUBLISHED)
        return qs.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog_owner"] = self.blog_owner
        context["blog_setting"] = BlogSetting.objects.filter(owner=self.blog_owner).first()
        return context

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('category', 'author').prefetch_related('tags')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # 让 /api/posts/<slug>/ 生效
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    # 让 filterset_fields / search_fields / ordering_fields 真正生效
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'category__slug', 'tags__slug']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'views']
    ordering = ['-created_at']  # 默认排序

    def _ensure_unique_slug(self, base_slug: str) -> str:
        """
        保证 slug 唯一：the-godfather -> the-godfather-xxxx
        """
        slug = base_slug or get_random_string(8)
        # 如果模型层已经 unique=True，这里更是保险；否则这里就是关键
        while Post.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{get_random_string(4)}"
        return slug

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title', '')
        base_slug = serializer.validated_data.get('slug') or slugify(title)
        slug = self._ensure_unique_slug(base_slug)
        serializer.save(author=self.request.user, slug=slug)

    def perform_update(self, serializer):
        """
        更新时：如果用户显式改了 slug，就也保证唯一；
        否则沿用原 slug。
        """
        new_slug = serializer.validated_data.get('slug', None)
        if new_slug is not None:
            new_slug = slugify(new_slug)
            if new_slug != self.get_object().slug:
                new_slug = self._ensure_unique_slug(new_slug)
            serializer.save(author=self.request.user, slug=new_slug)
        else:
            serializer.save(author=self.request.user)



class BlogSettingViewSet(viewsets.ModelViewSet):
    queryset = BlogSetting.objects.select_related('owner')
    serializer_class = BlogSettingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


class HomeView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/home.html'

    def get_queryset(self):
        qs = Post.objects.filter(status=Post.PUBLISHED).select_related('author', 'category').prefetch_related('tags')
        q = self.request.GET.get('q')
        category = self.request.GET.get('category')
        tag = self.request.GET.get('tag')
        ordering = self.request.GET.get('order', '-created_at')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(tags__name__icontains=q)).distinct()
        if category:
            qs = qs.filter(category__slug=category)
        if tag:
            qs = qs.filter(tags__slug=tag)
        if ordering not in ['-created_at', 'created_at', '-views', 'views']:
            ordering = '-created_at'
        return qs.order_by(ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['active_category'] = self.request.GET.get('category')
        context['active_tag'] = self.request.GET.get('tag')
        context['search_term'] = self.request.GET.get('q', '')
        context['ordering'] = self.request.GET.get('order', '-created_at')
        context['blog_setting'] = BlogSetting.objects.filter(owner=self.request.user).first() if self.request.user.is_authenticated else None
        context['hero_post'] = (
            Post.objects.filter(status=Post.PUBLISHED)
            .select_related('author', 'category')
            .prefetch_related('tags')
            .order_by('-views', '-created_at')
            .first()
        )
        context['trending_tags'] = (
            Tag.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')[:8]
        )
        User = get_user_model()
        context['insights'] = {
            'posts': Post.objects.filter(status=Post.PUBLISHED).count(),
            'authors': User.objects.count(),
            'comments': self.model.objects.filter(status=Post.PUBLISHED).aggregate(total=Count('comments'))['total']
            or 0,
            'tags': Tag.objects.count(),
        }
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Post.objects.select_related('author', 'category').prefetch_related('tags', 'comments__author')

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        Post.objects.filter(pk=self.object.pk).update(views=F('views') + 1)
        return response

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect(f"{reverse('accounts:login')}?next={request.path}")
        content = request.POST.get('content', '').strip()
        parent_id = request.POST.get('parent')
        if content:
            from comments.models import Comment

            parent = None
            if parent_id:
                parent = get_object_or_404(Comment, pk=parent_id, post=self.object)
            Comment.objects.create(post=self.object, author=request.user, content=content, parent=parent)
        return redirect(self.object.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = Post.objects.filter(status=Post.PUBLISHED, category=self.object.category).exclude(pk=self.object.pk)[:3]
        return context


class PostEditorView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        if 'slug' in kwargs:
            post = self.get_object()
            form = PostForm(instance=post)
        else:
            post = None
            form = PostForm()
        return render(request, self.template_name, {'form': form, 'post': post})

    def post(self, request, *args, **kwargs):
        post = None
        if 'slug' in kwargs:
            post = self.get_object()
            form = PostForm(request.POST, request.FILES, instance=post)
        else:
            form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if not post.slug:
                post.slug = slugify(post.title)
            post.save()
            form.save_m2m()
            return redirect(post.get_absolute_url())
        return render(request, self.template_name, {'form': form, 'post': post})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


class BlogSettingView(LoginRequiredMixin, DetailView):
    template_name = 'blog/settings.html'
    model = BlogSetting

    def get_object(self, queryset=None):
        setting, _ = BlogSetting.objects.get_or_create(owner=self.request.user)
        return setting

    def get(self, request, *args, **kwargs):
        setting = self.get_object()
        form = BlogSettingForm(instance=setting)
        return render(request, self.template_name, {'form': form, 'setting': setting})

    def post(self, request, *args, **kwargs):
        setting = self.get_object()
        form = BlogSettingForm(request.POST, request.FILES, instance=setting)
        if form.is_valid():
            form.save()
            return redirect('blog:blog-setting')
        return render(request, self.template_name, {'form': form, 'setting': setting})

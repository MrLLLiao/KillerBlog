from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BlogSettingView,
    BlogSettingViewSet,
    CategoryViewSet,
    HomeView,
    PostDetailView,
    PostEditorView,
    PostViewSet,
    TagViewSet,
    post_delete,
    UserBlogView,
)

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('tags', TagViewSet)
router.register('posts', PostViewSet)
router.register('settings', BlogSettingViewSet, basename='blog-setting')

app_name = 'blog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('u/<str:username>/', UserBlogView.as_view(), name='user-blog'),
    path('write/', PostEditorView.as_view(), name='post-create'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('write/', PostEditorView.as_view(), name='post-create'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<slug:slug>/edit/', PostEditorView.as_view(), name='post-edit'),
    path('posts/<slug:slug>/delete/', post_delete, name='post-delete'),
    path('settings/', BlogSettingView.as_view(), name='blog-setting'),
    path('api/', include((router.urls, 'blog_api'), namespace='blog_api')),
]

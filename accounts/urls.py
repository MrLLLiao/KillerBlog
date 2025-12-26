from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    UserDetailView,
    UserListCreateView,
    login_view,
    profile,
    profile_edit,
    register,
)

app_name = 'accounts'

urlpatterns = [
    path('api/', UserListCreateView.as_view(), name='user-list-create'),
    path('api/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', profile_edit, name='profile-edit'),
    path('profile/<str:username>/', profile, name='profile-detail'),
    path('profile/edit/', profile_edit, name='profile-edit'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
]

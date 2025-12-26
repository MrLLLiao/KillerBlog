from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='邮箱', required=True)
    avatar = forms.ImageField(label='头像', required=False)
    bio = forms.CharField(label='简介', widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'avatar', 'bio']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'bio']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'bio': forms.Textarea(attrs={'class': 'textarea', 'rows': 4}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='用户名或邮箱', widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class': 'input'}))

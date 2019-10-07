from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email

class ProfileCreateForm(forms.ModelForm):
    """プロフィール作成フォーム"""

    class Meta:
        model = Profile
        fields = ('user_name','user_nickname','image_profile','image_cover','user_from','user_address','user_text')
        widgets = {
        'user_text': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'わからないこと、解決したいことを10文字以上で書いてください',
        }),
        }

class ProfileUpdateForm(forms.ModelForm):
    """プロフィール更新フォーム"""

    class Meta:
        model = Profile
        fields = ('user_name','user_nickname','image_profile','image_cover','user_from','user_address','user_text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'



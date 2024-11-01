from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="ایمیل")

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class AuthenticationForm(auth_forms.AuthenticationForm):
    def confirm_login_allowed(self, user):
        super(AuthenticationForm,self).confirm_login_allowed(user)
        
        # if not user.is_verified:
        #     raise ValidationError("user is not verified")
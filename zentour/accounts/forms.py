from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter your email")

    def clean_email(self):
        new_email = self.cleaned_data.get("email")
        if User.objects.filter(email=new_email).exists():
            raise forms.ValidationError("This email already exists")
        else:
            return new_email

    class Meta:
        model = User
        extra_fields = ["email"]
        fields = [
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "email",
        ]


class LoginForm(forms.Form):
    username = UsernameField(label="Enter Username", max_length=100, required=True)
    password = forms.CharField(
        label="Enter Password", widget=forms.PasswordInput(), required=True
    )


class ProfileUpdateForm(forms.Form):
    email = forms.EmailField(label="Email:")
    avatar = forms.ImageField(required=False, label="Upload avatar:")

    def clean_email(self):
        new_email = self.cleaned_data.get("email")
        if User.objects.filter(email=new_email).exists():
            raise ValidationError("This email already exists")
        else:
            return new_email

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["email"].initial = self.user.email

from django import forms
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

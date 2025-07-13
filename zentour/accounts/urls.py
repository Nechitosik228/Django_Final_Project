from django.urls import path

from .views import register, login_view, logout_view, profile, edit_user_profile

app_name = "accounts"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile, name="profile"),
    path("edit_profile/", edit_user_profile, name="edit_profile"),
]

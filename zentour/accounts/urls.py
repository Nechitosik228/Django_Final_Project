from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from .views import register, login_view, logout_view, profile, edit_user_profile, superuser_view, become_superuser, top_up_balance, transactions

app_name = "accounts"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile, name="profile"),
    path("edit_profile/", edit_user_profile, name="edit_profile"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy("accounts:password_change_done"),
            template_name="accounts/password_change.html",
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/reset_password/form.html",
            email_template_name="accounts/emails/reset.html",
            success_url=reverse_lazy("accounts:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/reset_password/done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/reset_password/confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/reset_password/complete.html"
        ),
        name="password_reset_complete",
    ),
    path("superuser/", superuser_view, name='superuser_view'),
    path("become-superuser/", become_superuser, name='become_superuser'),
    path("top-up-balance/", top_up_balance, name='top_up_balance'),
    path("transactions/", transactions, name='transactions'),
]

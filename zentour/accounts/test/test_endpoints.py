import pytest
import uuid

from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages
from django.conf import settings

from .fixtures import test_image_file


@pytest.mark.django_db
def test_register_view_creates_user_and_redirects(client):
    url = reverse("accounts:register")

    form_data = {
        "username": "testuser123",
        "email": "test@example.com",
        "password1": "VeryStrongPassword123",
        "password2": "VeryStrongPassword123",
    }

    response = client.post(url, data=form_data)

    assert response.status_code == 302
    assert response.url == reverse("tours:home")
    assert User.objects.filter(username="testuser123").exists()


@pytest.mark.django_db
def test_login_view_success(client, user):

    url = reverse("accounts:login")
    form_data = {
        "username": user.username,
        "password": "password_test_user",
    }

    response = client.post(url, data=form_data)

    assert response.status_code == 302
    assert response.url == reverse("tours:home")


@pytest.mark.django_db
def test_login_view_wrong_password(client, user):

    url = reverse("accounts:login")
    form_data = {
        "username": user.username,
        "password": "WrongPass456",
    }

    response = client.post(url, data=form_data)

    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].errors
    assert "Invalid username or password." in response.content.decode()


@pytest.mark.django_db
def test_login_view_invalid_user(client):
    url = reverse("accounts:login")
    form_data = {
        "username": "nonexistent",
        "password": "anyPass123",
    }

    response = client.post(url, data=form_data)

    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].errors
    assert "Invalid username or password." in response.content.decode()


@pytest.mark.django_db
def test_logout_view(client, user):
    client.login(username=user.username, password="password_test_user")

    response = client.get(reverse("tours:home"))
    assert response.wsgi_request.user.is_authenticated

    response = client.get(reverse("accounts:logout"))

    assert response.status_code == 302
    assert response.url == reverse("tours:home")

    response = client.get(reverse("tours:home"))
    assert not response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_profile_view_authenticated(client, user):
    client.login(username=user.username, password="password_test_user")

    url = reverse("accounts:profile")
    response = client.get(url)

    assert response.status_code == 200
    assert "profile" in response.context
    assert str(response.context["profile"].user) == user.username
    assert b"profile" in response.content.lower()


@pytest.mark.django_db
def test_profile_view_unauthenticated(client):
    url = reverse("accounts:profile")
    response = client.get(url)

    assert response.status_code == 302
    assert response.url.startswith(reverse("accounts:login"))


@pytest.mark.django_db
def test_edit_user_profile_post_email_update(client, user):
    client.login(username=user.username, password="password_test_user")
    url = reverse("accounts:edit_profile")

    new_email = "updated@example.com"
    form_data = {
        "email": new_email,
    }

    response = client.post(url, data=form_data)

    user.refresh_from_db()
    assert response.status_code == 302
    assert response.url == reverse("accounts:profile")
    assert user.email == new_email


@pytest.mark.django_db
def test_edit_user_profile_post_avatar_update(client, user, test_image_file):
    client.login(username=user.username, password="password_test_user")
    url = reverse("accounts:edit_profile")

    new_email = "avatar_test@example.com"
    form_data = {
        "email": new_email,
        "avatar": test_image_file,
    }

    response = client.post(url, data=form_data, format="multipart")

    user.refresh_from_db()

    profile = user.profile

    assert response.status_code == 302
    assert response.url == reverse("accounts:profile")

    assert user.email == new_email

    assert profile.avatar
    assert "avatar" in profile.avatar.name
    assert profile.avatar.name.startswith("avatars/")
    assert profile.avatar.name.endswith(".jpg")


@pytest.mark.django_db
def test_edit_user_profile_get(client, user):
    client.login(username=user.username, password="password_test_user")
    url = reverse("accounts:edit_profile")

    response = client.get(url)

    assert response.status_code == 200
    assert "form" in response.context
    assert b"edit" in response.content.lower()


@pytest.mark.django_db
def test_transactions_view_unauthenticated(client):
    url = reverse("accounts:transactions")

    response = client.get(url)

    assert response.status_code == 302
    assert response.url.startswith(reverse("accounts:login"))


@pytest.mark.django_db
def test_transactions_view_authenticated(client, user):
    client.login(username=user.username, password="password_test_user")
    url = reverse("accounts:transactions")

    response = client.get(url)

    assert response.status_code == 200
    assert b"transactions" in response.content.lower()


@pytest.mark.django_db
def test_superuser_view_unauthenticated(client):
    url = reverse("accounts:superuser_view")

    response = client.get(url)

    assert response.status_code == 302
    assert reverse("accounts:login") in response.url


@pytest.mark.django_db
def test_superuser_view_regular_user(client, user):
    client.login(username=user.username, password="password_test_user")
    url = reverse("accounts:superuser_view")

    response = client.get(url)

    assert response.status_code == 200
    assert b"superuser" in response.content.lower()
    assert str(settings.SUPER_USER_PAYMENT).encode() in response.content


@pytest.mark.django_db
def test_superuser_view_superuser_redirects(client, super_user):
    client.login(username=super_user.username, password="Adminpasword123")

    url = reverse("accounts:superuser_view")
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse("accounts:profile")


@pytest.mark.django_db
def test_become_superuser_already_superuser(client, super_user):
    client.login(username=super_user.username, password="Adminpasword123")
    url = reverse("accounts:become_superuser")

    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse("accounts:profile")

    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert "You are already super user" in messages

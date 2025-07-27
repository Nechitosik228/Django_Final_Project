import pytest
import uuid

from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
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

import os
import pytest
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zentour.settings")
django.setup()

from django.contrib.auth.models import User


@pytest.fixture
def user(db):
    user = User.objects.create_user(
        username="testusertestusertestuser", password="password_test_user"
    )
    profile = user.profile
    profile.email_confirmed = True
    profile.save()
    return user


@pytest.fixture
def super_user():
    user = User.objects.create_superuser(
        username="Admin", password="Adminpasword123", email="admin@gmail.com"
    )
    user.profile.email_confirmed = True
    user.profile.save()
    return user

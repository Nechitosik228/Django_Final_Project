import os
import pytest
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zentour.settings")
django.setup()

from django.contrib.auth.models import User

@pytest.fixture
def user():
    return User.objects.create_user(
        username="testusertestusertestuser", password="password_test_user"
    )


@pytest.fixture
def super_user():
    return User.objects.create_superuser(
        username='Admin', 
        password='Adminpasword123', 
        email='admin@gmail.com'
    )
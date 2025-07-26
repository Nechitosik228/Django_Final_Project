import pytest

from django.contrib.auth.models import User

from accounts.models import Balance, Transaction, Profile
from tours.models import Cart, Order, Review, BoughtTour
from .fixtures import profile, balance


@pytest.mark.django_db
def test_profile_model(profile):
    assert isinstance(profile, Profile)
    assert profile.user.username == "testusertestusertestuser"
    assert profile.balance.amount == 0
    assert profile.avatar == "/avatars/default_avatar.jpg"


@pytest.mark.django_db
def test_profile_creation(user):
    profile = Profile.objects.get(user=user)
    cart = Cart.objects.get(user=user)
    balance = profile.balance

    assert isinstance(profile, Profile)
    assert profile.avatar == "/avatars/default_avatar.jpg"
    assert profile.user == user
    assert cart.user == user
    assert balance.amount == 0
    assert cart.items.count() == 0


@pytest.mark.django_db
def test_balance_top_up_and_save(user):
    balance = user.profile.balance

    assert balance.amount == 0

    balance.amount += 150
    balance.save()

    updated_balance = Balance.objects.get(id=balance.id)
    assert updated_balance.amount == 150

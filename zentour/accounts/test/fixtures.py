import pytest
from accounts.models import Balance, Transaction, Profile


@pytest.fixture
def profile(user):
    return user.profile


@pytest.fixture
def balance(profile):
    return profile.balance

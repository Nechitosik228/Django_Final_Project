import pytest
from accounts.models import Balance, Transaction, Profile


@pytest.fixture
def profile(user):
    return user.profile


@pytest.fixture
def balance(profile):
    return profile.balance


@pytest.fixture
def transaction(balance):
    return Transaction.objects.create(
        balance=balance,
        action=Transaction.Action.TOPING_UP,
        status=Transaction.Choices.NEW,
        money_amount=100,
        category="Test category",
    )

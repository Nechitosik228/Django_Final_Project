import pytest

from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from accounts.models import Balance, Transaction, Profile
from tours.models import Cart, Order, Review, BoughtTour
from .fixtures import (
    profile,
    balance,
    transaction,
    completed_transaction,
    completed_transaction_withdraw,
    transaction_default_category,
)


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


@pytest.mark.django_db
def test_transaction_creation(transaction, user):
    assert transaction.balance == user.profile.balance
    assert transaction.money_amount == 100
    assert transaction.status == Transaction.Choices.NEW
    assert transaction.action == Transaction.Action.TOPING_UP


@pytest.mark.django_db
def test_profile_related_balance_and_cart(user):
    profile = user.profile
    cart = Cart.objects.get(user=user)

    assert profile.balance.amount == 0
    assert cart.user == user


@pytest.mark.django_db
def test_profile_str(user):
    profile = user.profile
    assert str(profile) == user.username


@pytest.mark.django_db
def test_balance_str(user):
    balance = user.profile.balance
    assert str(balance) == f"Ballance: {balance.amount}"


@pytest.mark.django_db
def test_balance_updated_after_transaction(balance):
    Transaction.objects.create(
        balance=balance,
        action=Transaction.Action.TOPING_UP,
        status=Transaction.Choices.COMPLETED,
        money_amount=200,
        category="Test top up",
    )

    balance.amount += 200
    balance.save()

    updated = Balance.objects.get(id=balance.id)
    assert updated.amount == 200


@pytest.mark.django_db
def test_multiple_transactions_and_total(
    balance, completed_transaction, completed_transaction_withdraw, transaction
):

    completed_transactions = balance.transactions.filter(
        status=Transaction.Choices.COMPLETED
    )
    total_top_up = sum(
        t.money_amount
        for t in completed_transactions
        if t.action == Transaction.Action.TOPING_UP
    )
    total_withdraw = sum(
        t.money_amount
        for t in completed_transactions
        if t.action == Transaction.Action.WITHDRAWING
    )
    assert total_top_up == 100
    assert total_withdraw == 50


@pytest.mark.django_db
def test_user_profile_uniqueness(user):
    with pytest.raises(IntegrityError):
        Profile.objects.create(user=user, balance=Balance.objects.create())


@pytest.mark.django_db
def test_balance_cascade_deletes_transactions(
    balance, completed_transaction_withdraw, completed_transaction
):

    assert Transaction.objects.count() == 2

    balance.delete()

    assert Transaction.objects.count() == 0


@pytest.mark.django_db
def test_transaction_default_category(transaction_default_category):
    assert transaction_default_category.category == ""


@pytest.mark.django_db
def test_transaction_status_choices(transaction):
    assert transaction.status in [t.value for t in Transaction.Choices]


@pytest.mark.django_db
def test_transaction_action_choices(transaction):
    assert transaction.action in [t.value for t in Transaction.Action]

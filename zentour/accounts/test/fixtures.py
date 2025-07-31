import io
import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import Transaction


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


@pytest.fixture
def completed_transaction(balance):
    return Transaction.objects.create(
        balance=balance,
        action=Transaction.Action.TOPING_UP,
        status=Transaction.Choices.COMPLETED,
        money_amount=100,
        category="Test category",
    )


@pytest.fixture
def completed_transaction_withdraw(balance):
    return Transaction.objects.create(
        balance=balance,
        action=Transaction.Action.WITHDRAWING,
        status=Transaction.Choices.COMPLETED,
        money_amount=50,
        category="Withdraw",
    )


@pytest.fixture
def transaction_default_category(balance):
    return Transaction.objects.create(
        balance=balance,
        action=Transaction.Action.TOPING_UP,
        status=Transaction.Choices.NEW,
        money_amount=100,
    )


@pytest.fixture
def test_image_file():
    image = Image.new("RGB", (100, 100), color="red")
    byte_io = io.BytesIO()
    image.save(byte_io, "JPEG")
    byte_io.seek(0)
    return SimpleUploadedFile("avatar.jpg", byte_io.read(), content_type="image/jpeg")

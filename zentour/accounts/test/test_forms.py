import pytest

from accounts.forms import RegisterForm, LoginForm, BalanceForm, ProfileUpdateForm
from .fixtures import test_image_file


# @pytest.mark.django_db
# def test_register_form_valid_data():
#     form_data = {
#         "username": "newuser",
#         "first_name": "Test",
#         "last_name": "User",
#         "email": "newuser@example.com",
#         "password1": "StrongPass123!",
#         "password2": "StrongPass123!",
#     }
#     form = RegisterForm(data=form_data)
#     assert form.is_valid()


@pytest.mark.django_db
def test_register_form_missing_required_fields():
    form = RegisterForm(data={})
    assert not form.is_valid()
    expected_fields = ["username", "password1", "password2", "email"]
    for field in expected_fields:
        assert field in form.errors


def test_login_form_valid_data():
    form_data = {
        "username": "testuser",
        "password": "SecurePass123!",
    }
    form = LoginForm(data=form_data)
    assert form.is_valid()
    assert form.cleaned_data["username"] == "testuser"
    assert form.cleaned_data["password"] == "SecurePass123!"


def test_login_form_invalid_data():
    form_data = {
        "username": "a" * 101,
        "password": "",
    }
    form = LoginForm(data=form_data)

    assert not form.is_valid()
    assert "username" in form.errors
    assert "Ensure this value has at most 100 characters" in form.errors["username"][0]
    assert "password" in form.errors
    assert "This field is required." in form.errors["password"][0]


def test_login_form_missing_username():
    form_data = {
        "password": "SecurePass123!",
    }
    form = LoginForm(data=form_data)
    assert not form.is_valid()
    assert "username" in form.errors
    assert "This field is required." in form.errors["username"]


def test_login_form_missing_password():
    form_data = {
        "username": "testuser",
    }
    form = LoginForm(data=form_data)
    assert not form.is_valid()
    assert "password" in form.errors
    assert "This field is required." in form.errors["password"]


def test_login_form_empty_fields():
    form_data = {
        "username": "",
        "password": "",
    }
    form = LoginForm(data=form_data)
    assert not form.is_valid()
    assert "username" in form.errors
    assert "password" in form.errors


@pytest.mark.django_db
def test_balance_form_valid_amount():
    form_data = {"amount": 100}
    form = BalanceForm(data=form_data)
    assert form.is_valid()
    assert form.cleaned_data["amount"] == 100


@pytest.mark.django_db
def test_balance_form_zero_amount():
    form_data = {"amount": 0}
    form = BalanceForm(data=form_data)
    assert not form.is_valid()
    assert "amount" in form.errors
    assert "Amount must be greater than zero." in form.errors["amount"]


@pytest.mark.django_db
def test_balance_form_negative_amount():
    form_data = {"amount": -50}
    form = BalanceForm(data=form_data)
    assert not form.is_valid()
    assert "amount" in form.errors
    assert "Amount must be greater than zero." in form.errors["amount"]


@pytest.mark.django_db
def test_balance_form_missing_amount():
    form_data = {}
    form = BalanceForm(data=form_data)
    assert not form.is_valid()
    assert "amount" in form.errors


# @pytest.mark.django_db
# def test_profile_update_form_valid(user, test_image_file):
#     form_data = {
#         "email": "updated@example.com",
#     }
#     form_files = {
#         "avatar": test_image_file,
#     }
#     form = ProfileUpdateForm(data=form_data, files=form_files, user=user)

#     assert form.is_valid()
#     assert form.cleaned_data["email"] == "updated@example.com"
#     assert form.cleaned_data["avatar"] == test_image_file


@pytest.mark.django_db
def test_profile_update_form_initial_email(user):
    form = ProfileUpdateForm(user=user)
    assert form.fields["email"].initial == user.email

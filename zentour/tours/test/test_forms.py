import pytest

from datetime import date, timedelta
from django.core.exceptions import ValidationError

from accounts.test.fixtures import test_image_file
from tours.forms import TourForm, OrderForm, ReviewForm, EditTourForm
from tours.models import Tour, Order
from .fixtures import tour


@pytest.mark.django_db
def test_order_form_missing_required_fields():
    form = OrderForm(data={})
    assert not form.is_valid()
    required_fields = ["contact_name", "contact_phone", "contact_email", "address"]
    for field in required_fields:
        assert field in form.errors


@pytest.mark.django_db
def test_order_form_invalid_email():
    form_data = {
        "contact_name": "John Doe",
        "contact_phone": "+380123456789",
        "contact_email": "invalid-email",
        "address": "123 Main Street",
    }
    form = OrderForm(data=form_data)
    assert not form.is_valid()
    assert "contact_email" in form.errors
    assert "Enter a valid email address." in form.errors["contact_email"]


@pytest.mark.django_db
def test_order_form_valid_data(user):
    form_data = {
        "contact_name": "John Doe",
        "contact_phone": "+380123456789",
        "contact_email": "john@example.com",
        "address": "123 Main Street, Kyiv",
    }
    form = OrderForm(data=form_data)
    assert form.is_valid()

    order = form.save(commit=False)
    order.user = user
    order.save()

    assert order.contact_name == "John Doe"
    assert order.contact_email == "john@example.com"
    assert order.user == user


@pytest.mark.django_db
def test_review_form_valid_data(user, tour):
    form_data = {
        "comment": "Great tour, really enjoyed it!",
        "rating": 4,
    }
    form = ReviewForm(data=form_data)
    assert form.is_valid()

    review = form.save(commit=False)
    review.user = user
    review.tour = tour
    review.save()

    assert review.pk is not None
    assert review.user == user
    assert review.tour == tour
    assert review.comment == form_data["comment"]
    assert review.rating == form_data["rating"]


@pytest.mark.django_db
def test_review_form_missing_required_fields():
    form = ReviewForm(data={})
    assert not form.is_valid()
    assert "comment" in form.errors
    assert "rating" in form.errors


@pytest.mark.django_db
def test_review_form_non_numeric_rating():
    form = ReviewForm(data={"comment": "ok", "rating": "not-a-number"})
    assert not form.is_valid()
    assert "rating" in form.errors


@pytest.mark.django_db
def test_review_form_comment_too_long(user, tour):
    long_comment = "x" * 301
    form = ReviewForm(data={"comment": long_comment, "rating": 3})
    assert not form.is_valid()
    assert "comment" in form.errors
    assert any("at most 300 characters" in msg for msg in form.errors["comment"])


@pytest.mark.django_db
def test_edit_tour_form_valid_data(tour, test_image_file):
    future_date = date.today() + timedelta(days=10)
    future_date_str = future_date.strftime("%Y-%m-%d")

    future_end_date = future_date + timedelta(days=30)
    future_end_date_str = future_end_date.strftime("%Y-%m-%d")

    form_data = {
        "name": "Updated Tour Name",
        "description": "Updated description",
        "start_date": future_date_str,
        "end_date": future_end_date_str,
        "price": 200,
        "discount": 5,
        "tickets_amount": 15,
        "cities": "Paris, Rome",
    }
    files = {"image": test_image_file}

    form = EditTourForm(data=form_data, files=files, instance=tour)
    if not form.is_valid():
        print(form.errors)

    assert form.is_valid()

    updated_tour = form.save()

    assert updated_tour.name == "Updated Tour Name"
    assert updated_tour.description == "Updated description"
    assert str(updated_tour.start_date) == future_date_str
    assert str(updated_tour.end_date) == future_end_date_str

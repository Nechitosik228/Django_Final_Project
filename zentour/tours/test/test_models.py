import pytest
import datetime

from django.contrib.auth.models import User
from django.urls import reverse

from accounts.models import Profile
from tours.models import Cart, Tour, Review, CartItem, Order, OrderItem
from .fixtures import tour, tour_with_discount, tour_with_no_tickets, cart_item, cart_item_with_discount


@pytest.mark.django_db
def test_tour_model(tour):
    assert tour.discount == 0
    assert tour.rating == None
    assert tour.discount_price == tour.price
    assert tour.available == True


@pytest.mark.django_db
def test_tour_with_discount_model(tour_with_discount):
    assert tour_with_discount.discount == 10
    assert tour_with_discount.discount_price == 45


@pytest.mark.django_db
def test_tour_with_no_tickets_model(tour_with_no_tickets):
    assert tour_with_no_tickets.tickets_amount == 0
    assert tour_with_no_tickets.available == False


@pytest.mark.django_db
def test_tour_updated_at_model(tour):
    tour.name = 'Test_name'
    tour.save()
    assert tour.updated_at == datetime.date.today()


@pytest.mark.django_db
def test_tour_created_at_model(user):
    tour = Tour.objects.create(
        user=user,
        name='Test name1',
        description='Test description',
        start_date='2025-01-01',
        end_date='2025-02-01',
        price=50,
        tickets_amount=20,
        cities='Berlin'
    )
    assert tour.created_at == datetime.date.today()

@pytest.mark.django_db
def test_cart_auto_creation_model(user):
    assert user.cart


@pytest.mark.django_db
def test_tour_cartitem_model(user, tour, cart_item):
    assert cart_item.tour == tour
    assert cart_item.amount == 1
    assert cart_item.total_price == tour.discount_price
    assert cart_item in user.cart.items.all()

@pytest.mark.django_db
def test_tour_two_cartitem_model(user, cart_item_with_discount, cart_item):
    assert cart_item_with_discount, cart_item in user.cart.items.all()
    assert cart_item_with_discount.total_price == cart_item_with_discount.tour.discount_price * cart_item_with_discount.amount
    assert user.cart.total == sum(item.total_price for item in user.cart.items.all())
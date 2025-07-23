import pytest

from django.contrib.auth.models import User
from django.urls import reverse

from accounts.models import Profile
from tours.models import Cart, Tour, Review, CartItem, Order, OrderItem
from .fixtures import tour, tour_with_discount, tour_with_no_tickets


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
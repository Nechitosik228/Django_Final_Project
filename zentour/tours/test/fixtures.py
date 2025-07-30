import pytest

from tours.models import Tour, Review, Cart, CartItem, Order, OrderItem


@pytest.fixture
def tour(user):
    return Tour.objects.create(
        user=user,
        name="Test name",
        description="Test description",
        start_date="2025-01-01",
        end_date="2025-02-01",
        price=50,
        tickets_amount=20,
        cities='Berlin',
        image='avatars/logo.png'
    )


@pytest.fixture
def tour_with_discount(user):
    return Tour.objects.create(
        user=user,
        name="Test2 name",
        description="Test description",
        start_date="2025-01-01",
        end_date="2025-02-01",
        price=50,
        discount=10,
        tickets_amount=20,
        cities="Berlin",
    )


@pytest.fixture
def tour_with_no_tickets(user):
    return Tour.objects.create(
        user=user,
        name="Test3 name",
        description="Test description",
        start_date="2025-01-01",
        end_date="2025-02-01",
        price=50,
        discount=10,
        tickets_amount=0,
        cities="Berlin",
    )


@pytest.fixture
def cart_item(user, tour):
    return CartItem.objects.create(cart=user.cart, tour=tour, amount=1)


@pytest.fixture
def cart_item_with_discount(user, tour_with_discount):
    return CartItem.objects.create(
        cart=user.cart,
        tour=tour_with_discount,
        amount=3
    )


@pytest.fixture
def review(user, tour):
    return Review.objects.create(
        user=user,
        tour=tour,
        comment='Test comment',
        rating=4.6
    )
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


@pytest.mark.django_db
def test_cart_two_items_total_model(tour, tour_with_discount):
    user = User.objects.create(
        username='Some name',
        password='some password'
    )
    
    cart_item1 = CartItem.objects.create(
        cart=user.cart,
        tour=tour,
        amount=2
    )

    cart_item2 = CartItem.objects.create(
        cart=user.cart,
        tour=tour_with_discount,
        amount=3
    )

    two_cart_items_price = 0
    two_cart_items_price += cart_item1.total_price
    two_cart_items_price += cart_item2.total_price

    assert user.cart.total == two_cart_items_price

@pytest.mark.django_db
def test_cart_one_item_total_model(tour):
    user = User.objects.create(
        username='Some name',
        password='some password'
    )
    
    cart_item1 = CartItem.objects.create(
        cart=user.cart,
        tour=tour,
        amount=2
    )

    assert user.cart.total == cart_item1.total_price


@pytest.mark.django_db
def test_cart_item_total_price_model(tour, cart_item):
    assert tour.discount_price * cart_item.amount == cart_item.total_price

@pytest.mark.django_db
def test_cart_item_default_amount_model(tour):
    user = User.objects.create(
        username='Some name',
        password='some password'
    )

    cart_item = CartItem.objects.create(
        tour=tour,
        cart=user.cart
    )

    assert cart_item.amount == 1

@pytest.mark.django_db
def test_cart_item_str_function_model(cart_item):
    assert cart_item.__str__() == f'{cart_item.tour.name}: {cart_item.amount}'


@pytest.mark.django_db
def test_order_default_fields_model(user):
    order = Order.objects.create(
        user=user,
        contact_name='Vasya',
        contact_email='example@gmail.com',
        address='Some address'
    )

    assert order.is_paid == False
    assert not order.items.all() 
    assert order.contact_phone == "000-000-0000"
    assert order in user.orders.all()


@pytest.mark.django_db
def test_order_total_model(user, tour):
    order = Order.objects.create(
        user=user,
        contact_name='Vasya',
        contact_email='example@gmail.com',
        address='Some address'
    )

    order_item1 = OrderItem.objects.create(
        order=order,
        tour=tour
    )

    assert order_item1.amount == 1
    assert order.total == order_item1.item_total
    assert order.total == tour.discount_price


@pytest.mark.django_db
def test_order_two_items_total_model(user, tour, tour_with_discount):
    order = Order.objects.create(
        user=user,
        contact_name='Vasya',
        contact_email='example@gmail.com',
        address='Some address'
    )

    order_item1 = OrderItem.objects.create(
        order=order,
        tour=tour
    )

    order_item2 = OrderItem.objects.create(
        order=order,
        tour=tour_with_discount,
    )

    assert order_item2.item_total == tour_with_discount.discount_price
    assert order_item1.item_total == tour.price
    assert order.total == sum(order_item.item_total for order_item in order.items.all())


@pytest.mark.django_db
def test_review_creation_model(tour, user):
    review = Review.objects.create(
        user=user,
        tour=tour,
        comment='Test comment',
        rating=4.5
    )

    assert review == Review.objects.get(id=1)
    assert review in tour.reviews.all()
    assert tour.rating == 4.5


@pytest.mark.django_db
def test_two_review_tour_rating_model(tour, user):
    user2 = User.objects.create(
        username='Username',
        password='Password'
    )

    review = Review.objects.create(
        user=user,
        tour=tour,
        comment='Test comment',
        rating=4.5
    )

    review2 = Review.objects.create(
        user=user2,
        tour=tour,
        comment='Test comment',
        rating=2.0
    )

    assert tour.rating == 3.2
    assert review, review2 in tour.reviews.all()
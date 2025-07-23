import pytest

from tours.models import Tour, Review, Cart, CartItem, Order, OrderItem

@pytest.fixture
def tour(user):
    return Tour.objects.create(
        user=user,
        name='Test name',
        description='Test description',
        start_date='01.01.2025',
        end_date='02.01.2025',
        price=50,
        tickets_amount=20,
        cities='Berlin'
    ) 
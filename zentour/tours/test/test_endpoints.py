import pytest
import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils.http import urlencode

from accounts.models import Profile
from tours.models import Cart, Tour, Review, CartItem, Order, OrderItem
from .fixtures import (
    tour,
    tour_with_discount,
    tour_with_no_tickets,
    cart_item,
    cart_item_with_discount,
)


@pytest.mark.django_db
def test_create_tour_endpoint_not_authorized(client):
    url = reverse("tours:create_tour")

    form_data = {
        "name": "Test name",
        "description": "Test description",
        "price": 1,
        "tickets_amount": 2,
        "cities": "Berlin",
        "start_date": "2025-08-30",
        "end_date": "2025-09-30",
    }

    response = client.post(url, data=form_data)

    url_login = reverse('accounts:login')
    url_with_query = f"{url_login}?next=/tours/create-tour/"

    assert response.status_code == 302
    assert response.url == url_with_query
    assert not Tour.objects.filter(name='Test name')


# @pytest.mark.django_db
# def test_create_tour_endpoint(client, super_user):
#     client.login(username='Admin', password='Adminpasword123')

#     url = reverse("tours:create_tour")

#     form_data = {
#         "name": "Test name",
#         "description": "Test description",
#         "price": 1,
#         "tickets_amount": 2,
#         "cities": "Berlin",
#         "start_date": "2025-08-30",
#         "end_date": "2025-09-30",
#     }

#     response = client.post(url, data=form_data)

#     messages = [m.error for m in get_messages(response.wsgi_request)]
#     print(messages)
#     print(response.serialize_headers())
#     assert response.status_code == 200


# @pytest.mark.django_db
# def test_get_tour_endpoint(client, tour):
#     url = reverse('tours:tour_detail', args=[tour.id])

#     response = client.get(url)

#     assert response.status_code == 200


@pytest.mark.django_db
def test_cart_not_authorized(client):
    url = reverse('tours:cart_detail')

    response = client.get(url)

    url_login = reverse('accounts:login')
    url_with_query = f"{url_login}?next=/tours/cart/"

    assert response.status_code == 302
    assert response.url == url_with_query


@pytest.mark.django_db
def test_cart_add_not_found(client, tour):
    url = 'tours/cart-add/1345'

    response = client.get(url)

    assert response.status_code == 404


# @pytest.mark.django_db
# def test_cart_add_not_authorized(client):
#     url = '/tours/cart-add/1'

#     response = client.post(url)

#     assert response.status_code == 301


@pytest.mark.django_db
def test_cart_delete_not_found(client, tour):
    url = 'tours/cart-delete/1345'

    response = client.get(url)

    assert response.status_code == 404
    
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


@pytest.mark.django_db
def test_create_tour_endpoint(client, super_user):
    client.login(username='Admin', password='Adminpasword123')

    url = reverse("tours:create_tour")

    form_data = {
        "name": "Test name",
        "description": "Test description",
        "discount":50,
        "price": 1,
        "tickets_amount": 2,
        "cities": "Berlin",
        "start_date": "2025-08-30",
        "end_date": "2025-09-30",
    }

    response = client.post(url, data=form_data)

    assert response.status_code == 302
    assert response.url == reverse('tours:tour_detail', args=[1])


@pytest.mark.django_db
def test_get_tour_endpoint(client, tour):
    url = reverse('tours:tour_detail', args=[tour.id])

    response = client.get(url)

    assert response.status_code == 200
    assert tour.name in response.content.decode()


@pytest.mark.django_db
def test_get_tour_not_found_endpoint(client, tour):
    url = reverse('tours:tour_detail', args=[320982390])

    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_cart_not_authorized(client):
    url = reverse('tours:cart_detail')

    response = client.get(url)

    url_login = reverse('accounts:login')
    url_with_query = f"{url_login}?next=/tours/cart/"

    assert response.status_code == 302
    assert response.url == url_with_query


@pytest.mark.django_db
def test_cart_add_not_found(client, tour, super_user):
    client.login(username=super_user.username, password='Adminpasword123')

    url = reverse('tours:cart_add', args=[1245])

    response = client.post(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_cart_add_not_authorized(client, tour):
    url = reverse('tours:cart_add', args=[tour.id])

    response = client.post(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_cart_delete_not_found(client, super_user):
    client.login(username=super_user.username, password='Adminpasword123')

    url = reverse('tours:cart_delete', args=[1234])

    response = client.get(url)

    assert response.status_code == 404
    

@pytest.mark.django_db
def test_cart_delete_not_authorized(client, tour):
    url = reverse('tours:cart_delete', args=[tour.id])

    response = client.post(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_review_creation_not_authorized(client, tour):
    url = reverse('tours:submit_review', args=[tour.id])

    data = {
        'comment':'Test comment',
        'rating': 4.5
    }

    response = client.post(url, data=data)

    assert response.status_code == 302


@pytest.mark.django_db
def test_review_creation(client, tour, super_user):
    client.login(username=super_user.username, password='Adminpasword123')

    url = reverse('tours:submit_review', args=[tour.id])

    data = {
        'comment':'Test comment',
        'rating': 4.5
    }

    response = client.post(url, data=data)

    assert response.status_code == 302
    assert response.url == reverse('tours:tour_detail', args=[tour.id])

    assert Review.objects.get(tour=tour)
    assert Review.objects.get(tour=tour).comment == data.get('comment')
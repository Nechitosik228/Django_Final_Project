import pytest

from django.urls import reverse
from django.contrib.messages import get_messages

from tours.models import Tour, Review, CartItem
from .fixtures import (
    tour,
    tour_with_discount,
    tour_with_no_tickets,
    cart_item,
    cart_item_with_discount,
    review,
)


@pytest.mark.django_db
def test_homepage(client):
    url = reverse("tours:home")

    response = client.get(url)

    assert response.status_code == 200
    assert response.wsgi_request.path == "/tours/home/"


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

    url_login = reverse("accounts:login")
    url_with_query = f"{url_login}?next=/tours/create-tour/"

    assert response.status_code == 302
    assert response.url == url_with_query
    assert not Tour.objects.filter(name="Test name")


@pytest.mark.django_db
def test_create_tour_endpoint(client, super_user):
    client.login(username="Admin", password="Adminpasword123")

    url = reverse("tours:create_tour")

    form_data = {
        "name": "Test name",
        "description": "Test description",
        "discount": 50,
        "price": 1,
        "tickets_amount": 2,
        "cities": "Berlin",
        "start_date": "2025-08-30",
        "end_date": "2025-09-30",
    }

    response = client.post(url, data=form_data)

    assert response.status_code == 302
    assert response.url == reverse("tours:tour_detail", args=[1])
    assert Tour.objects.filter(name=form_data.get("name")).exists()


@pytest.mark.django_db
def test_create_tour_not_valid_endpoint(client, super_user):
    client.login(username="Admin", password="Adminpasword123")

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

    assert "id_discount_error" in response.content.decode()
    assert "This field is required." in response.content.decode()
    assert response.context["form"].errors


@pytest.mark.django_db
def test_get_tour_endpoint(client, tour):
    url = reverse("tours:tour_detail", args=[tour.id])

    response = client.get(url)

    assert response.status_code == 200
    assert tour.name in response.content.decode()


@pytest.mark.django_db
def test_get_tour_not_found_endpoint(client, tour):
    url = reverse("tours:tour_detail", args=[320982390])

    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_cart_not_authorized(client):
    url = reverse("tours:cart_detail")

    response = client.get(url)

    url_login = reverse("accounts:login")
    url_with_query = f"{url_login}?next=/tours/cart/"

    assert response.status_code == 302
    assert response.url == url_with_query


@pytest.mark.django_db
def test_cart(client, super_user):
    client.login(username=super_user.username, password="Adminpasword123")

    url = reverse("tours:cart_detail")

    response = client.get(url)

    assert response.status_code == 200
    assert response.wsgi_request.path == "/tours/cart/"
    assert "Your cart is empty" in response.content.decode()


@pytest.mark.django_db
def test_cart_add_not_found(client, tour, super_user):
    client.login(username=super_user.username, password="Adminpasword123")

    url = reverse("tours:cart_add", args=[1245])

    response = client.post(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_cart_add_not_authorized(client, tour):
    url = reverse("tours:cart_add", args=[tour.id])

    response = client.post(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_cart_add(client, tour, super_user):
    client.login(username=super_user.username, password="Adminpasword123")

    url = reverse("tours:cart_add", args=[tour.id])

    response = client.post(url)

    assert response.status_code == 302
    assert CartItem.objects.filter(tour=tour).exists()


@pytest.mark.django_db
def test_cart_delete(client, tour, super_user):
    client.login(username=super_user.username, password="Adminpasword123")
    client.post(reverse("tours:cart_add", args=[tour.id]))

    url = reverse("tours:cart_delete", args=[tour.id])

    response = client.post(url)

    assert response.status_code == 302
    assert not CartItem.objects.filter(tour=tour)


@pytest.mark.django_db
def test_cart_delete_not_found(client, super_user):
    client.login(username=super_user.username, password="Adminpasword123")

    url = reverse("tours:cart_delete", args=[1234])

    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_cart_delete_not_authorized(client, tour):
    url = reverse("tours:cart_delete", args=[tour.id])

    response = client.post(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_review_creation_not_authorized(client, tour):
    url = reverse("tours:submit_review", args=[tour.id])

    data = {"comment": "Test comment", "rating": 4.5}

    response = client.post(url, data=data)

    assert response.status_code == 302


@pytest.mark.django_db
def test_review_creation(client, tour, super_user):
    client.login(username=super_user.username, password="Adminpasword123")

    url = reverse("tours:submit_review", args=[tour.id])

    data = {"comment": "Test comment", "rating": 4.5}

    response = client.post(url, data=data)

    assert response.status_code == 302
    assert response.url == reverse("tours:tour_detail", args=[tour.id])

    assert Review.objects.get(tour=tour)
    assert Review.objects.get(tour=tour).comment == data.get("comment")


@pytest.mark.django_db
def test_review_creation_not_valid(client, tour, super_user):
    client.login(username=super_user.username, password="Adminpasword123")

    url = reverse("tours:submit_review", args=[tour.id])

    data = {"rating": 4.5}

    response = client.post(url, data=data)

    assert "id_comment_error" in response.content.decode()


@pytest.mark.django_db
def test_review_creation_tour_not_found(client, super_user):
    client.login(username=super_user.username, password="Adminpasword123")

    url = reverse("tours:submit_review", args=[24432])

    data = {"comment": "Test comment", "rating": 4.5}

    response = client.post(url, data=data)

    assert response.status_code == 404


@pytest.mark.django_db
def test_checkout_not_authorized(client):
    url = reverse("tours:checkout")

    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_checkout_empty_cart(client, super_user):
    client.login(username=super_user.username, password="Adminpasword123")

    url = reverse("tours:checkout")

    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse("tours:cart_detail")
    assert "Your cart is empty" in [
        m.message for m in get_messages(response.wsgi_request)
    ]


@pytest.mark.django_db
def test_checkout_get(client, super_user, tour):
    client.login(username=super_user.username, password="Adminpasword123")
    client.post(reverse("tours:cart_add", args=[tour.id]))

    url = reverse("tours:checkout")

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_checkout_post_not_enough_money(client, super_user, tour):
    client.login(username=super_user.username, password="Adminpasword123")
    client.post(reverse("tours:cart_add", args=[tour.id]))

    url = reverse("tours:checkout")

    data = {
        "contact_name": "Test name",
        "contact_phone": "000-0000-000",
        "contact_email": "nikitanechitailo@gmail.com",
        "address": "Test address",
    }

    response = client.post(url, data=data)

    assert response.status_code == 302
    assert response.url == reverse("accounts:profile")
    assert "You don't have enough money on you balance" in [
        m.message for m in get_messages(response.wsgi_request)
    ]


@pytest.mark.django_db
def test_checkout_post(client, super_user, tour):
    client.login(username=super_user.username, password="Adminpasword123")
    client.post(reverse("tours:cart_add", args=[tour.id]))
    client.post(reverse("accounts:top_up_balance"), data={"amount": 100})

    url = reverse("tours:checkout")

    data = {
        "contact_name": "Test name",
        "contact_phone": "000-0000-000",
        "contact_email": "nikitanechitailo@gmail.com",
        "address": "Test address",
    }

    response = client.post(url, data=data)

    assert response.status_code == 302
    assert response.url == reverse("tours:home")
    assert "You have completed your order" in [
        m.message for m in get_messages(response.wsgi_request)
    ]


@pytest.mark.django_db
def test_tour_editing_not_authorized(client, super_user, tour):
    url = reverse("tours:tour_edit", args=[tour.id])

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

    url_login = reverse("accounts:login")
    url_with_query = f"{url_login}?next=/tours/edit/1/"

    assert response.status_code == 302
    assert response.url == url_with_query


@pytest.mark.django_db
def test_tour_editing_not_author(client, super_user, tour):
    client.login(username=super_user.username, password="Adminpasword123")

    url = reverse("tours:tour_edit", args=[tour.id])

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

    assert response.status_code == 302
    assert response.url == reverse("tours:tour_detail", args=[tour.id])
    assert "This is not your tour" in [
        m.message for m in get_messages(response.wsgi_request)
    ]


@pytest.mark.django_db
def test_tour_editing(client, user, tour):
    client.login(username=user.username, password="password_test_user")

    url = reverse("tours:tour_edit", args=[tour.id])

    form_data = {
        "name": "Testname",
        "description": "Test description",
        "discount": 50,
        "price": 1,
        "tickets_amount": 2,
        "cities": "Berlin",
        "start_date": "2025-08-30",
        "end_date": "2025-09-30",
    }

    response = client.post(url, data=form_data)

    assert response.status_code == 302
    assert response.url == reverse("tours:tour_detail", args=[tour.id])
    assert "Tour updated successfully." in [
        m.message for m in get_messages(response.wsgi_request)
    ]
    assert Tour.objects.get(id=tour.id).name == "Testname"


@pytest.mark.django_db
def test_tour_deleting_not_authorized(client, tour):
    url = reverse("tours:delete_tour", args=[tour.id])

    response = client.post(url)

    url_login = reverse("accounts:login")
    url_with_query = f"{url_login}?next=/tours/delete/1/"

    assert response.status_code == 302
    assert response.url == url_with_query


@pytest.mark.django_db
def test_tour_deleting_not_author(client, super_user, tour):
    client.login(username=super_user.username, password="Adminpasword123")

    url = reverse("tours:delete_tour", args=[tour.id])

    response = client.post(url)

    assert response.status_code == 302
    assert response.url == reverse("tours:tour_detail", args=[tour.id])
    assert "You are not the creator of this tour!" in [
        m.message for m in get_messages(response.wsgi_request)
    ]


@pytest.mark.django_db
def test_tour_deleting_get(client, user, tour):
    client.login(username=user.username, password="password_test_user")

    url = reverse("tours:delete_tour", args=[tour.id])

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_tour_deleting_post(client, user, tour):
    client.login(username=user.username, password="password_test_user")

    url = reverse("tours:delete_tour", args=[tour.id])

    data = {"answer": "Yes"}

    response = client.post(url, data=data)

    assert response.status_code == 302
    assert response.url == reverse("tours:home")
    assert "You deleted your tour" in [
        m.message for m in get_messages(response.wsgi_request)
    ]


@pytest.mark.django_db
def test_review_deleting_not_authorized(client, review):
    url = reverse("tours:delete_review", args=[review.id])

    response = client.get(url)

    url_login = reverse("accounts:login")
    url_with_query = f"{url_login}?next=/tours/delete_review/1/"

    assert response.status_code == 302
    assert response.url == url_with_query


@pytest.mark.django_db
def test_review_deleting_not_author(client, super_user, review):
    client.login(username=super_user.username, password="Adminpasword123")

    url = reverse("tours:delete_review", args=[review.id])

    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse("tours:tour_detail", args=[review.tour.id])
    assert "You are not the creator of this review!" in [
        m.message for m in get_messages(response.wsgi_request)
    ]


@pytest.mark.django_db
def test_review_deleting_get(client, user, review):
    client.login(username=user.username, password="password_test_user")

    url = reverse("tours:delete_review", args=[review.id])

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_review_deleting_post(client, user, review):
    client.login(username=user.username, password="password_test_user")

    url = reverse("tours:delete_review", args=[review.id])

    data = {"answer": "Yes"}
    response = client.post(url, data=data)

    assert response.status_code == 302
    assert response.url == reverse("tours:tour_detail", args=[review.tour.id])
    assert "You deleted your review" in [
        m.message for m in get_messages(response.wsgi_request)
    ]

from django.urls import path

from .views import (
    home,
    create_tour,
    tour_detail,
    cart_detail,
    cart_add,
    cart_delete,
    submit_review,
    checkout,
    tour_editing,
    delete_tour,
    delete_review,
    users_bought_tours,
)


app_name = "tours"


urlpatterns = [
    path("home/", home, name="home"),
    path("create-tour/", create_tour, name="create_tour"),
    path("tour/<int:tour_id>/", tour_detail, name="tour_detail"),
    path("cart/", cart_detail, name="cart_detail"),
    path("cart-add/<int:tour_id>/", cart_add, name="cart_add"),
    path("cart-delete/<int:tour_id>/", cart_delete, name="cart_delete"),
    path("submit-review/<int:tour_id>/", submit_review, name="submit_review"),
    path("checkout/", checkout, name="checkout"),
    path("edit/<int:tour_id>/", tour_editing, name="tour_edit"),
    path("delete/<int:tour_id>/", delete_tour, name="delete_tour"),
    path("delete_review/<int:review_id>/", delete_review, name="delete_review"),
    path("bought_tours/", users_bought_tours, name="users_bought_tours"),
]

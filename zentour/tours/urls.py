from django.urls import path

from .views import home, create_tour, tour_detail, cart_detail, cart_add, cart_delete, submit_review, checkout


app_name = "tours"


urlpatterns = [
    path("home/", home, name="home"),
    path("create-tour/", create_tour, name="create_tour"),
    path("tour/<int:tour_id>/", tour_detail, name="tour_detail"),
    path("cart/", cart_detail, name='cart_detail'),
    path("cart-add/<int:tour_id>/", cart_add, name='cart_add'),
    path("cart-delete/<int:tour_id>/", cart_delete, name='cart_delete'),
    path("submit-review/<int:tour_id>/", submit_review, name="submit_review"),
    path("checkout/", checkout, name="checkout")
]

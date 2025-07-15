from django.urls import path

from .views import home, create_tour, tour_detail, cart_detail


app_name = "tours"


urlpatterns = [
    path("home/", home, name="home"),
    path("create-tour/", create_tour, name="create_tour"),
    path("tour/<int:tour_id>", tour_detail, name="tour_detail"),
    path("cart/", cart_detail, name='cart_detail')
]

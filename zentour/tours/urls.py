from django.urls import path
from .views import (
    home,
    create_tour
)


app_name = "tours"


urlpatterns = [
    path("home/", home, name="home"),
    path("create-tour/", create_tour, name="create_tour")
]
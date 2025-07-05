from django.urls import path

from .views import home

app_name = "tours"

urlpatterns = [
    path("", home, name="home"),
]

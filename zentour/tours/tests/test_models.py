import pytest

from django.contrib.auth.models import User
from django.urls import reverse

from accounts.models import Profile
from tours.models import Cart, Tour, Review, CartItem, Order, OrderItem
from .fixtures import tour
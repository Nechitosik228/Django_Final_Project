import pytest
import datetime

from django.contrib.auth.models import User
from django.urls import reverse

from accounts.models import Profile
from tours.models import Cart, Tour, Review, CartItem, Order, OrderItem
from .fixtures import (
    tour,
    tour_with_discount,
    tour_with_no_tickets,
    cart_item,
    cart_item_with_discount,
)

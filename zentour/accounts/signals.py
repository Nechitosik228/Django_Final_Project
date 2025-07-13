from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Profile, Balance
from tours.models import Cart


@receiver(post_save, sender=User)
def create_user_profile_and_cart_and_balance(sender, instance, created, **kwargs):
    if created:
        balance = Balance.objects.create()
        Cart.objects.create(user=instance)
        Profile.objects.create(user=instance, balance=balance)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Balance


@receiver(post_save, sender=User)
def create_user_profile_and_cart(sender, instance, created, **kwargs):
    if created:
        balance = Balance.objects.create()
        Profile.objects.create(user=instance, balance=balance)

from django.db import models
from django.contrib.auth.models import User


class Balance(models.Model):
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    balance = models.OneToOneField(Balance, on_delete=models.CASCADE)

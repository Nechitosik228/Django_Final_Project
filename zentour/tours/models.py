from django.db import models
from django.contrib.auth.models import User


class Tour(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image_path = models.ImageField(upload_to="tour_images/")
    discount = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    tickets_amount = models.IntegerField()
    cities = models.CharField(max_length=250)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    @property
    def discount_price(self):
        if self.discount:
            return self.price - self.price * self.discount / 100
        else:
            return self.price

    class Meta:
        ordering = ["-end_date"]
        db_table = "tours"

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def total(self):
        return sum(item.item_total for item in self.items.all())

    def __str__(self):
        return f"{self.user.username}'s cart"
    
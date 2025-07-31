import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Tour(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="tours", null=True
    )
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to="tour_images/", null=True)
    discount = models.PositiveIntegerField(default=0)
    tickets_amount = models.PositiveIntegerField()
    cities = models.CharField(max_length=250)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    @property
    def discount_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        else:
            return self.price

    @property
    def rating(self):
        all_review = self.reviews.all()
        if all_review.exists():
            return round(
                sum(review.rating for review in all_review) / all_review.count(), 1
            )

    @property
    def available(self):
        if self.tickets_amount > 0:
            return True
        else:
            return False

    class Meta:
        ordering = ["-end_date"]
        db_table = "tours"

    def clean(self):
        if self.end_date and self.start_date:
            if self.end_date <= self.start_date:
                raise ValidationError(
                    {"end_date": "End date should be after the start date"}
                )
            if self.start_date < datetime.date.today():
                raise ValidationError({"start_date": "Start date cannot be in past"})
        if self.discount > 100:
            raise ValidationError({"discount": "Discount cannot be higher than 100%"})
        if self.price <= 0:
            raise ValidationError({"price": "Price should be higher than 0"})

    def __str__(self):
        return self.name


class BoughtTour(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="bought_tours", null=True
    )
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True)


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="reviews", null=True
    )
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="reviews")
    comment = models.TextField(max_length=300)
    rating = models.FloatField()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f"{self.user.username}'s cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.amount * self.tour.discount_price

    def __str__(self):
        return f"{self.tour.name}: {self.amount}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    contact_name = models.CharField(max_length=50)
    contact_phone = models.CharField(max_length=20, default="000-000-0000")
    contact_email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)

    class Choices(models.IntegerChoices):
        NEW = 1
        PROCESSING = 2
        SHIPPED = 3
        COMPLETED = 4
        CANCELED = 5

    status = models.IntegerField(choices=Choices, default=Choices.NEW)

    @property
    def total(self):
        return sum([item.item_total for item in self.items.all()])


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", null=True
    )
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    @property
    def item_total(self):
        return self.tour.discount_price * self.amount

    def __str__(self):
        return (
            f"{self.order.id} : {self.tour.name} : {self.amount} : ${self.item_total}"
        )

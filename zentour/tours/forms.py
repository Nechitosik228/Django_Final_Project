from django import forms
from .models import Tour, Order, Review


class TourForm(forms.ModelForm):
    start_date = forms.DateField(
        input_formats=["%d/%m/%Y"], widget=forms.DateInput(format="%d/%m/%Y")
    )

    end_date = forms.DateField(
        input_formats=["%d/%m/%Y"], widget=forms.DateInput(format="%d/%m/%Y")
    )

    image = forms.ImageField(required=True, label="Upload an image:")

    class Meta:
        model = Tour
        extra_fields = ["start_date", "end_date", "image"]
        fields = [
            "name",
            "description",
            "price",
            "discount",
            "tickets_amount",
            "cities",
        ]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["contact_name", "contact_phone", "contact_email", "address"]

        labels = {
            "contact_name": "Enter your name",
            "contact_phone": "Enter your phone number",
            "contact_email": "Enter your email",
            "address": "Enter your address",
        }


class ReviewForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 4, "placeholder": "Leave your feedback here..."}
        ),
        label="Your Review",
    )

    rating = forms.FloatField(
        widget=forms.NumberInput(attrs={"min": 0, "max": 5, "step": 1}),
        label="Rating (0–5)",
    )

    class Meta:
        model = Review
        fields = ["comment", "rating"]

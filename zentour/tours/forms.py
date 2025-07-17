from django import forms
from .models import Tour, Review


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


class ReviewForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 4, "placeholder": "Leave your feedback here..."}
        ),
        label="Your Review",
    )

    rating = forms.FloatField(
        widget=forms.NumberInput(attrs={"min": 0, "max": 5, "step": 0.5}),
        label="Rating (0–5)",
    )

    class Meta:
        model = Review
        fields = ["comment", "rating"]

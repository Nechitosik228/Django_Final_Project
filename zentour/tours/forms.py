from django import forms
from .models import Tour


class TourForm(forms.ModelForm):
    start_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(format='%d/%m/%Y')
    )

    end_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(format='%d/%m/%Y')
    )

    image = forms.ImageField(required=True, label='Upload an image:')

    class Meta:
        model = Tour
        extra_fields = [
            'start_date',
            'end_date',
            'image'
        ]
        fields = [
            "name",
            "description",
            "price",
            "discount",
            "tickets_amount",
            "cities"
        ]

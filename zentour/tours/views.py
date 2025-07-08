from django.shortcuts import render

from .models import Tour


def home(request):
    tours = Tour.objects.all()

    filter = request.GET.get("filter")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if min_price:
        tours = tours.filter(price__gte=min_price)
    if max_price:
        tours = tours.filter(price__lte=max_price)

    if start_date:
        tours = tours.filter(start_date__gte=start_date)
    if end_date:
        tours = tours.filter(end_date__lte=end_date)

    if filter == "decrease_price":
        tours = tours.order_by("-price")
    elif filter == "increase_price":
        tours = tours.order_by("price")
    elif filter == "increase_rating":
        tours = tours.order_by("rating")
    elif filter == "decrease_rating":
        tours = tours.order_by("-rating")

    return render(request, 'tours/home.html', context={'tours': tours})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Tour
from .forms import TourForm


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


@login_required
def create_tour(request):
    # if request.user.is_superuser == True:
    if request.method == "GET":
        form = TourForm()
    else:
        form = TourForm(request.POST, request.FILES)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            image = form.cleaned_data.get('image')
            tour = form.save(commit=False)
            tour.user = request.user
            tour.start_date = start_date
            tour.end_date = end_date
            tour.image = image
            tour.save()
            messages.success(request, 'You have created your Tour') 
            return redirect('tours:home')
        

    return render(request, 'tours/create_tour.html', {'form':form})
    # else:
    #     messages.warning(request, 'You are not a super user!')
    #     return redirect('tours:home')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Tour, CartItem, OrderItem, Review
from .forms import TourForm, ReviewForm, OrderForm


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
            print(form.cleaned_data)
            print(image)
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


def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    return render(request, "tours/tour_detail.html", {"tour": tour})


@login_required
def cart_detail(request):
    cart = request.user.cart
    if not cart.items.count():
        items = []
    else:
        items = cart.items.select_related("tour").all()
    print(cart)

    return render(request, "tours/cart.html", {"cart": cart, "items": items})


@login_required
def cart_delete(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    cart = request.user.cart
    cart_item = CartItem.objects.get(cart=cart, tour=tour)
    cart_item.amount -= 1
    if cart_item.amount == 0:
        cart_item.delete()
    else:
        cart_item.save()
    return redirect("tours:cart_detail")


@login_required
def cart_add(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    cart = request.user.cart
    cart_item, create = CartItem.objects.get_or_create(cart=cart, tour=tour)
    if create:
        cart_item.amount = 1
    else:
        cart_item.amount += 1
    cart_item.save()
    return redirect('tours:cart_detail')


@login_required
def checkout(request):
    if not getattr(request.user, 'cart', None):
        messages.error(request, 'Your cart is empty')
        return redirect('tours:cart_detail')
    if request.method == 'GET':
        form = OrderForm()
        form.initial['contact_email'] = request.user.email
        form.initial['contact_name'] = request.user.first_name
    else:
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            cart = getattr(request.user, 'cart')
            cart_items = cart.items.select_related('tour').all()
            OrderItem.objects.bulk_create(
                [
                    OrderItem(
                        order=order,
                        tour=item.tour,
                        amount=item.amount,
                        price=item.tour.discount_price
                    )
                    for item in cart_items
                ]
            )
            if order.total <= request.user.profile.balance.amount:
                order.status = 2
                request.user.profile.balance.amount -= order.total
                order.is_paid = True
                order.save()
            else:
                order.status = 5
                order.save()
                messages.error(request, "You don't have enough money on you balance")
                return redirect('accounts:profile')
            messages.success(request, 'You have completed your order')
            return redirect('tours:home')
    return render(request, 'tours/checkout.html', {'form':form})


@login_required
def submit_review(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    try:
        review = tour.reviews.get(user=request.user)
        is_edit = True
    except Review.DoesNotExist:
        review = None
        is_edit = False

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.tour = tour
            review.save()
            msg = (
                "Your review has been updated."
                if is_edit
                else "Your review has been added."
            )
            messages.success(request, msg)
            return redirect("tours:tour_detail", tour_id=tour.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, "tours/tour_detail.html", {"form": form, "tour": tour})
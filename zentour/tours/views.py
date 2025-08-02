from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage

from .models import Tour, CartItem, OrderItem, Review, BoughtTour
from .forms import TourForm, ReviewForm, OrderForm, EditTourForm
from .utils import calculate_star_ranges, create_transaction, send_email_with_attachment
from accounts.utils.decorator import email_confirmed_required


def home(request):
    tours = Tour.objects.all()

    filter = request.GET.get("filter")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    search = request.GET.get("search")

    if search:
        tours = tours.filter(name__icontains=search)

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

    for tour in tours:
        stars = calculate_star_ranges(tour.rating)
        tour.full_stars = stars["full_stars"]
        tour.has_half_star = stars["has_half_star"]
        tour.empty_stars = stars["empty_stars"]

    return render(request, "tours/home.html", context={"tours": tours})


@login_required
@email_confirmed_required
def create_tour(request):
    if request.user.is_superuser == True:
        if request.method == "GET":
            form = TourForm()
        else:
            form = TourForm(request.POST, request.FILES)
            if form.is_valid():
                start_date = form.cleaned_data.get("start_date")
                end_date = form.cleaned_data.get("end_date")
                image = form.cleaned_data.get("image")
                tour = form.save(commit=False)
                tour.user = request.user
                tour.start_date = start_date
                tour.end_date = end_date
                tour.image = image
                tour.save()
                messages.success(request, "You have created your Tour")
                return redirect("tours:tour_detail", tour_id=tour.id)

        return render(request, "tours/create_tour.html", {"form": form})
    else:
        messages.warning(request, "You are not a super user!")
        return redirect("accounts:superuser_view")


def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour.objects.prefetch_related("reviews__user"), id=tour_id)
    form = ReviewForm() if request.user.is_authenticated else None

    stars = calculate_star_ranges(tour.rating)

    for review in tour.reviews.all():
        review_stars = calculate_star_ranges(review.rating)
        review.full_stars = review_stars["full_stars"]
        review.has_half_star = review_stars["has_half_star"]
        review.empty_stars = review_stars["empty_stars"]

    return render(
        request,
        "tours/tour_detail.html",
        {
            "tour": tour,
            "form": form,
            "full_stars": stars["full_stars"],
            "has_half_star": stars["has_half_star"],
            "empty_stars": stars["empty_stars"],
        },
    )


@login_required
@email_confirmed_required
def tour_editing(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.user != tour.user:
        messages.warning(request, "This is not your tour")
        return redirect("tours:tour_detail", tour_id=tour.id)

    if request.method == "POST":
        form = EditTourForm(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            form.save()
            messages.success(request, "Tour updated successfully.")
            return redirect("tours:tour_detail", tour_id=tour.id)
    else:
        form = EditTourForm(instance=tour)
    return render(request, "tours/edit_tour.html", {"form": form, "tour": tour})


@login_required
@email_confirmed_required
def delete_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.user != tour.user:
        messages.error(request, "You are not the creator of this tour!")
        return redirect("tours:tour_detail", tour_id=tour_id)

    if request.method == "GET":
        return render(request, "tours/delete_tour.html", {"tour": tour})
    else:
        if request.POST.get("answer") == "Yes":
            bought_tours = BoughtTour.objects.filter(tour=tour).all()
            if bought_tours:
                for bought_tour in bought_tours:
                    bought_tour.user.profile.balance.amount += bought_tour.price
                    bought_tour.user.profile.balance.save()
                    create_transaction(
                        bought_tour.user.profile.balance,
                        1,
                        bought_tour.price,
                        f"Tour {tour} tickets return",
                        4,
                    )
                    request.user.profile.balance.amount -= bought_tour.price
                    request.user.profile.balance.save()
                    create_transaction(
                        request.user.profile.balance,
                        2,
                        bought_tour.price,
                        f"Tour {tour} tickets return",
                        4,
                    )
            tour.delete()
            messages.success(request, "You deleted your tour")
            return redirect("tours:home")
        else:
            return redirect("tours:tour_detail", tour_id=tour_id)


@login_required
@email_confirmed_required
def users_bought_tours(request):
    bought_tours = request.user.bought_tours.all()
    return render(request, "tours/users_tours.html", {"bought_tours": bought_tours})


@login_required
@email_confirmed_required
def cart_detail(request):
    cart = request.user.cart
    if not cart.items.count():
        items = []
    else:
        items = cart.items.select_related("tour").all()

    return render(request, "tours/cart.html", {"cart": cart, "items": items})


@login_required
@email_confirmed_required
def cart_delete(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    cart = request.user.cart
    cart_item = get_object_or_404(CartItem, cart=cart, tour=tour)
    cart_item.amount -= 1
    if cart_item.amount == 0:
        cart_item.delete()
    else:
        cart_item.save()
    return redirect("tours:cart_detail")


@login_required
@email_confirmed_required
def cart_add(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    cart = request.user.cart
    cart_item, create = CartItem.objects.get_or_create(cart=cart, tour=tour)
    if create:
        if tour.tickets_amount > 0:
            cart_item.amount = 1
        else:
            cart_item.delete()
            messages.warning(
                request,
                f"Tickets left for {tour}: {tour.tickets_amount}. You cannot buy this tour!",
            )
            return redirect("tours:tour_detail", tour_id=tour.id)
    else:
        cart_item.amount += 1
        if tour.tickets_amount < cart_item.amount:
            messages.warning(
                request,
                f"Tickets left for {tour}: {tour.tickets_amount}. You cannot add another ticket!",
            )
            return redirect("tours:cart_detail")
        else:
            cart_item.save()

    cart_item.save()
    return redirect("tours:cart_detail")


@login_required
@email_confirmed_required
def checkout(request):
    if not request.user.cart.items.all():
        messages.error(request, "Your cart is empty")
        return redirect("tours:cart_detail")
    if request.method == "GET":
        form = OrderForm()
        form.initial["contact_email"] = request.user.email
        form.initial["contact_name"] = request.user.first_name
    else:
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            cart = getattr(request.user, "cart")
            cart_items = cart.items.select_related("tour").all()
            order_items = OrderItem.objects.bulk_create(
                [
                    OrderItem(
                        order=order,
                        tour=item.tour,
                        amount=item.amount,
                    )
                    for item in cart_items
                ]
            )
            balance = request.user.profile.balance
            if order.total <= balance.amount:
                order.status = 2
                balance.amount -= order.total
                balance.save()
                for order_item in order_items:
                    create_transaction(
                        balance,
                        2,
                        order_item.item_total,
                        f"Tour {order_item.tour} purchase",
                        status=4,
                    )
                    order_item.tour.tickets_amount -= order_item.amount
                    order_item.tour.save()
                    order_item.tour.user.profile.balance.amount += order_item.item_total
                    order_item.tour.user.profile.balance.save()
                    create_transaction(
                        order_item.tour.user.profile.balance,
                        1,
                        order_item.item_total,
                        f"Profit from Tour {order_item.tour}",
                        status=4,
                    )
                    bought_tour, create = BoughtTour.objects.get_or_create(
                        user=request.user,
                        tour=order_item.tour,
                    )
                    send_email_with_attachment(
                        "Tickets",
                        f"Hello! Here is/are your {order_item.amount} ticket/s for {order_item.tour} in a PDF file:",
                        settings.EMAIL_HOST_USER,
                        [order.contact_email],
                        order_item,
                        bought_tour
                    )
                    if create:
                        bought_tour.price = order_item.item_total
                        bought_tour.amount = order_item.amount
                        bought_tour.save()
                    else:
                        bought_tour.amount += order_item.amount
                        bought_tour.price += order_item.item_total
                        bought_tour.save()
                order.is_paid = True
                order.save()
                cart.items.all().delete()
            else:
                order.status = 5
                order.save()
                create_transaction(balance, 2, order.total, "Tour purchase", status=5)
                messages.error(request, "You don't have enough money on you balance")
                return redirect("accounts:profile")
            messages.success(
                request,
                "You have completed your order. We have sent tickets to your email",
            )
            return redirect("tours:home")
    return render(request, "tours/checkout.html", {"form": form})


@login_required
@email_confirmed_required
def submit_review(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.user == tour.user:
        messages.error(request, "You cannot leave a review to your own tour")
        return redirect("tours:tour_detail", tour_id=tour.id)

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


@login_required
@email_confirmed_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.user != review.user:
        messages.error(request, "You are not the creator of this review!")
        return redirect("tours:tour_detail", tour_id=review.tour.id)

    if request.method == "GET":
        return render(request, "tours/delete_review.html")
    else:
        if request.POST.get("answer") == "Yes":
            review.delete()
            messages.success(request, "You deleted your review")
            return redirect("tours:tour_detail", tour_id=review.tour.id)
        else:
            return redirect("tours:tour_detail", tour_id=review.tour.id)

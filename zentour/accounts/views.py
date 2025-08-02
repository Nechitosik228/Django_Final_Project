from django.conf import settings
from django.urls import reverse
from django.http import Http404
from django.contrib import messages
from django.utils.http import urlencode
from django.core.mail import send_mail
from django.core.signing import SignatureExpired
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, ProfileUpdateForm, BalanceForm
from accounts.models import Profile
from accounts.utils.decorator import email_confirmed_required
from tours.utils import create_transaction


def send_confirmation_email(request, user, new_email: str | None = None):
    profile = user.profile
    if new_email:
        token = profile.generate_email_confirmation_token(for_new_email=new_email)
        email_to = new_email
    else:
        token = profile.generate_email_confirmation_token()
        email_to = user.email

    confirm_url = request.build_absolute_uri(
        reverse("accounts:confirm_email") + "?" + urlencode({"token": token})
    )
    subject = "Підтвердження email"
    message = (
        f"Hello {user.username},\n\n"
        f"Please confirm your email address by clicking on the link:\n{confirm_url}\n\n"
        "If you haven't done this, ignore this letter."
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email_to],
        fail_silently=False,
    )


def confirm_email(request):
    token = request.GET.get("token")
    if not token:
        raise Http404("No token provided")
    try:
        user_pk, email_to_confirm = Profile.validate_email_confirmation_token(token)
    except SignatureExpired:
        messages.error(request, "The token has expired. Request a new confirmation.")
        return redirect("accounts:profile")
    except Exception:
        messages.error(request, "Invalid token.")
        return redirect("accounts:profile")
    try:
        user = User.objects.get(pk=user_pk)
        profile = user.profile
    except User.DoesNotExist:
        raise Http404()

    if profile.pending_email and email_to_confirm == profile.pending_email:
        user.email = profile.pending_email
        user.save()
        profile.pending_email = ""
    elif email_to_confirm != user.email:
        messages.error(request, "Токен не відповідає email.")
        return redirect("accounts:profile")

    profile.email_confirmed = True
    profile.save()
    messages.success(request, "Email успішно підтверджено.")
    return redirect("accounts:profile")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            user.profile.email_confirmed = False
            user.profile.save()
            login(request, user)
            send_confirmation_email(request, user)
            messages.info(
                request,
                "Registered. Check your email and confirm your email address to gain full access.",
            )
            return redirect("tours:home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("tours:home")
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("tours:home")


@login_required
def profile(request):
    profile = request.user.profile
    return render(request, "accounts/profile.html", {"profile": profile})


@login_required
def edit_user_profile(request):
    user = request.user
    profile = user.profile
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if email and email != user.email:
                profile.email_confirmed = False
                profile.save()
                send_confirmation_email(request, user, new_email=email)
                messages.info(
                    request,
                    "Your new email has been sent for confirmation. Check it and click on the link.",
                )
            avatar = form.cleaned_data.get("avatar")
            if avatar:
                profile.avatar = avatar
            profile.save()
            return redirect("accounts:profile")
    else:
        form = ProfileUpdateForm(user=user)

    return render(
        request, "accounts/edit_profile.html", {"form": form, "profile": profile}
    )


@login_required
@email_confirmed_required
def superuser_view(request):
    if request.user.is_superuser == True:
        messages.success(request, "You are already super user")
        return redirect("accounts:profile")
    return render(
        request, "accounts/superuser.html", {"payment": settings.SUPER_USER_PAYMENT}
    )


@login_required
@email_confirmed_required
def become_superuser(request):
    super_user_payment = settings.SUPER_USER_PAYMENT
    balance = request.user.profile.balance
    if request.user.is_superuser == True:
        messages.success(request, "You are already super user")
        return redirect("accounts:profile")
    if balance.amount < super_user_payment:
        create_transaction(
            balance, 2, super_user_payment, "Super user payment", status=5
        )
        messages.error(request, "You do not have enough money")
        return redirect("accounts:profile")

    balance.amount -= super_user_payment
    balance.save()
    request.user.is_superuser = True
    request.user.save()
    create_transaction(balance, 2, super_user_payment, "Super user payment", status=4)

    messages.success(request, "Now you are a superuser and can create your own tour!")
    return redirect("accounts:profile")


@login_required
@email_confirmed_required
def top_up_balance(request):
    if request.method == "GET":
        form = BalanceForm()
    else:
        form = BalanceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get("amount")
            balance = request.user.profile.balance
            balance.amount += amount
            balance.save()
            create_transaction(balance, 1, amount, "Balance toping up", status=4)
            messages.success(request, f"You have topped up your balance with ${amount}")
            return redirect("accounts:profile")
    return render(request, "accounts/balance.html", {"form": form})


@login_required
@email_confirmed_required
def transactions(request):
    return render(request, "accounts/transactions.html")

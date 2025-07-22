from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, LoginForm, ProfileUpdateForm, BalanceForm
from tours.utils import create_transaction

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
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
                user.email = email
                user.save()
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
def superuser_view(request):
    if request.user.is_superuser == True:
        messages.success(request, 'You are already super user')
        return redirect('accounts:profile')
    return render(request, 'accounts/superuser.html', {'payment': settings.SUPER_USER_PAYMENT})

    
@login_required
def become_superuser(request):
    super_user_payment = settings.SUPER_USER_PAYMENT
    balance = request.user.profile.balance
    if request.user.is_superuser == True:
        messages.success(request, 'You are already super user')
        return redirect('accounts:profile')
    if balance.amount < super_user_payment:
        create_transaction(balance, 2, super_user_payment, 'Super user payment', status=5)
        messages.error(request, 'You do not have enough money')
        return redirect('accounts:profile')
        
    balance.amount -= super_user_payment
    balance.save()
    request.user.is_superuser = True
    request.user.save()
    create_transaction(balance, 2, super_user_payment, 'Super user payment', status=4)

    messages.success(request, 'Now you are a superuser and can create your own tour!')
    return redirect('accounts:profile')


@login_required
def top_up_balance(request):
    if request.method == 'GET':
        form = BalanceForm()
    else:
        form = BalanceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            balance = request.user.profile.balance
            balance.amount += amount
            balance.save()
            create_transaction(balance, 1, amount, 'Balance toping up', status=4)
            messages.success(request, f'You have topped up your balance with ${amount}')
            return redirect('accounts:profile')
    return render(request, 'accounts/balance.html', {'form':form})
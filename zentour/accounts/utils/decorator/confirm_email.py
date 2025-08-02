from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def email_confirmed_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.profile.email_confirmed:
            messages.warning(
                request,
                "You need to confirm your email address to use this feature. Please check your email.",
            )
            return redirect("accounts:profile")
        return view_func(request, *args, **kwargs)

    return _wrapped

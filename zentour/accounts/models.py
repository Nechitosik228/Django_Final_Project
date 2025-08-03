from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired


class Balance(models.Model):
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Ballance: {self.amount}"


class Transaction(models.Model):
    class Choices(models.IntegerChoices):
        NEW = 1
        PROCESSING = 2
        SHIPPED = 3
        COMPLETED = 4
        CANCELED = 5

    class Action(models.IntegerChoices):
        TOPING_UP = 1
        WITHDRAWING = 2

    status = models.IntegerField(choices=Choices, default=Choices.NEW)
    action = models.IntegerField(choices=Action, default=Action.TOPING_UP)
    balance = models.ForeignKey(
        Balance, on_delete=models.CASCADE, related_name="transactions"
    )
    category = models.CharField(max_length=200, default="")
    money_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(
        upload_to="avatars/",
        default="/avatars/default_avatar.jpg",
        blank=True,
        null=True,
    )
    balance = models.OneToOneField(Balance, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    pending_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def generate_email_confirmation_token(self, for_new_email: str | None = None):
        signer = TimestampSigner()
        data = self.user.pk

        if for_new_email:
            value = f"{data}:{for_new_email}"
        else:
            value = f"{data}:{self.user.email}"
        return signer.sign(value)

    @staticmethod
    def validate_email_confirmation_token(token, max_age=60 * 60 * 1):
        signer = TimestampSigner()
        try:
            unsigned = signer.unsign(token, max_age=max_age)
        except SignatureExpired:
            raise
        except BadSignature:
            raise

        try:
            user_pk_str, email = unsigned.split(":", 1)
            return int(user_pk_str), email
        except ValueError:
            raise BadSignature("Malformed token")

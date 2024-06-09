import uuid
from django.db import models
from django.utils import timezone

# Create your models here.


def generate_id():
    return uuid.uuid4().hex


class Payment(models.Model):
    """
    Model for storing payments.
    """

    STATUS = (
        ("scheduled", "Scheduled"),
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    )
    id = models.CharField(
        primary_key=True, editable=False, default=generate_id, max_length=70
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="NGN")
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        related_name="payments",
    )
    status = models.CharField(max_length=10, choices=STATUS, default="pending")
    reference = models.CharField(max_length=256, null=True, blank=True)
    paystack_payment_id = models.CharField(
        max_length=256, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class ScheduledPayment(models.Model):
    STATUS = (
        ("scheduled", "Scheduled"),
        ("failed", "failed"),
        ("fullfilled", "Fullfilled"),
    )
    id = models.CharField(
        primary_key=True, editable=False, default=generate_id, max_length=70
    )

    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        related_name="scheduled_payments",
    )
    status = models.CharField(
        max_length=10, choices=STATUS, default="scheduled"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="NGN")
    description = models.TextField(null=True, blank=True)
    schedule_date = models.DateTimeField(timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Wallet(models.Model):
    """
    Model for storing wallets.
    """

    id = models.CharField(
        primary_key=True, editable=False, default=generate_id, max_length=70
    )
    user = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, related_name="wallets"
    )
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=1000000
    )  # setting default value to allow user schedule payment
    currency = models.CharField(max_length=3, default="NGN")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Wallet"

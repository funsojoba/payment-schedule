import uuid
from django.db import models

# Create your models here.

def generate_id():
    return uuid.uuid4().hex



class Payment(models.Model):
    """
    Model for storing payments.
    """
    STATUS = (
        ('scheduled', 'Scheduled'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )
    id = models.CharField(
        primary_key=True, editable=False, default=generate_id, max_length=70
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    schedule_date = models.DateTimeField()
    user = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='payments'
    )
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id



class Wallet(models.Model):
    """
    Model for storing wallets.
    """
    id = models.CharField(
        primary_key=True, editable=False, default=generate_id, max_length=70
    )
    user = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='wallets'
    )
    total_amount = models.DecimalField( max_digits=10, decimal_places=2, default=1000000) # setting default value to allow user schedule payment
    currency = models.CharField(max_length=3, default="NGN")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Wallet"
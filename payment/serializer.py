from rest_framework import serializers

from .models import Payment, Wallet, ScheduledPayment


class PostSchedulePaymentSerializer(serializers.Serializer):
    """
    Serializer for scheduling a payment.
    """

    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3)
    schedule_date = serializers.DateTimeField()


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for payments.
    """

    class Meta:
        model = Payment
        fields = "__all__"


class WalletSerializer(serializers.ModelSerializer):
    """
    Serializer for wallets.
    """

    class Meta:
        model = Wallet
        fields = "__all__"


class SchedulePaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for Scheduled Payment model
    """

    schedule_date = serializers.DateTimeField(format="%B %d, %Y, %I:%M %p")

    class Meta:
        model = ScheduledPayment
        fields = "__all__"

from rest_framework import serializers

from .models import Payment, Wallet



class SchedulePaymentSerializer(serializers.Serializer):
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
        fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):
    """
    Serializer for wallets.
    """
    class Meta:
        model = Wallet
        fields = '__all__'
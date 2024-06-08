from rest_framework import serializers



class SchedulePaymentSerializer(serializers.Serializer):
    """
    Serializer for scheduling a payment.
    """

    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3)
    schedule_date = serializers.DateTimeField()
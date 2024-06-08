from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets, permissions

from django.db import transaction
from django.db.models import F

from drf_yasg.utils import swagger_auto_schema

from .serializer import SchedulePaymentSerializer

from .models import Payment, Wallet



class PaymentView(viewsets.ViewSet):
    """
    API endpoint that allows users perform authentications.
    """
    authentication_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Schedule a payment",
        operation_summary="Schedule a payment",
        tags=["Payment"],
        request_body=SchedulePaymentSerializer,
    )
    @action(methods=['post'], detail=False)
    def schedule_payment(self, request):
        """
        Schedule a payment.
        """

        serializer = SchedulePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = float(serializer.validated_data.get('amount'))
        currency = serializer.validated_data.get('currency')
        schedule_date = serializer.validated_data.get('schedule_date')

        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(user=request.user, currency=currency)
            
            if wallet.total_amount < amount:
                raise ValidationError("Insufficient funds in the wallet.")
            
            payment = Payment.objects.create(
                user=request.user,
                amount=amount,
                currency=currency,
                schedule_date=schedule_date
            )
            
            wallet.total_amount = F('total_amount') - amount
            wallet.save()

            return Response(status=status.HTTP_200_OK, data={
                'payment_id': payment.id,
                'wallet_id': wallet.id,
                'total_amount': wallet.total_amount,
                "message": "Payment scheduled successfully."
            })
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets, permissions

from rest_framework.exceptions import ValidationError

from django.db import transaction
from django.db.models import F

from drf_yasg.utils import swagger_auto_schema

from .serializer import SchedulePaymentSerializer, PaymentSerializer, WalletSerializer

from .models import Payment, Wallet



class PaymentView(viewsets.ViewSet):
    """
    API endpoint that allows users perform authentications.
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Schedule a payment",
        operation_summary="Schedule a payment",
        tags=["Payment"],
        request_body=SchedulePaymentSerializer,

    )
    @action(methods=['POST'], detail=False)
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
                raise ValidationError(detail={"error":"Insufficient funds in the wallet."})
            
            payment = Payment.objects.create(
                user=request.user,
                amount=amount,
                currency=currency,
                schedule_date=schedule_date,
                status='scheduled'
            )
            
            wallet.total_amount = F('total_amount') - amount
            wallet.save()

            return Response(status=status.HTTP_200_OK, data={
                "message": "Payment scheduled successfully."
            })

    @swagger_auto_schema(
        operation_description="Get scheduled payments",
        operation_summary="Get scheduled payments",
        tags=["Payment"],
    )
    @action(methods=['GET'], detail=False)
    def scheduled_payments(self, request):
        """
        Get scheduled payments.
        """
        scheduled_payments = Payment.objects.filter(user=request.user, status='scheduled')
        return Response(status=status.HTTP_200_OK, data={
            "message": "Scheduled payments retrieved successfully.",
            "data": PaymentSerializer(scheduled_payments, many=True).data})


    @swagger_auto_schema(
        operation_description="Get wallet",
        operation_summary="Get wallet",
        tags=["Payment"],
    )
    @action(methods=['GET'], detail=False)
    def wallet(self, request):
        """
        Get wallet.
        """
        wallet = Wallet.objects.filter(user=request.user).first()
        return Response(status=status.HTTP_200_OK, data={
            "message": "Wallet retrieved successfully.",
            "data": WalletSerializer(wallet).data})
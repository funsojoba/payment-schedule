from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets, permissions

from rest_framework.exceptions import ValidationError

from django.db import transaction
from django.db.models import Sum

from drf_yasg.utils import swagger_auto_schema

from .serializer import (
    PostSchedulePaymentSerializer,
    # PaymentSerializer,
    WalletSerializer,
    SchedulePaymentSerializer,
)

from .models import Wallet, ScheduledPayment

from notification.service import EmailService


class PaymentView(viewsets.ViewSet):
    """
    API endpoint that allows users perform authentications.
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Schedule a payment",
        operation_summary="Schedule a payment",
        tags=["Payment"],
        request_body=PostSchedulePaymentSerializer,
    )
    @action(methods=["POST"], detail=False)
    def schedule_payment(self, request):
        """
        Schedule a payment. No deduction is made yet,
        users can see their wallet balance and how much is
        scheduled to be deducted and date
        """

        serializer = PostSchedulePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = float(serializer.validated_data.get("amount"))
        currency = serializer.validated_data.get("currency")
        schedule_date = serializer.validated_data.get("schedule_date")

        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(
                user=request.user, currency=currency
            )

            schedule_payments = ScheduledPayment.objects.filter(
                user=request.user, status="scheduled"
            )
            total_scheduled_payment = (
                schedule_payments.aggregate(total=Sum("amount"))["total"] or 0
            )

            # Check if wallet balance is greater than amount to be scheduled,
            # and all the amount that has been scheduled
            if (float(total_scheduled_payment) + amount) > wallet.total_amount:
                raise ValidationError(
                    detail={"error": "Insufficient funds in the wallet."}
                )

            ScheduledPayment.objects.create(
                amount=amount, user=request.user, schedule_date=schedule_date
            )

            EmailService.send_async(
                template="payment_scheduled.html",
                subject="Payment Scheduled Successfully",
                recipients=[request.user.email],
                context={
                    "name": request.user.display_name,
                    "currency": wallet.currency,
                    "amount": amount,
                    "schedule_date": schedule_date,
                },
            )

            return Response(
                status=status.HTTP_200_OK,
                data={"message": "Payment scheduled successfully."},
            )

    @swagger_auto_schema(
        operation_description="Get scheduled payments",
        operation_summary="Get scheduled payments",
        tags=["Payment"],
    )
    @action(methods=["GET"], detail=False)
    def scheduled_payments(self, request):
        """
        Get scheduled payments.
        """
        scheduled_payments = ScheduledPayment.objects.filter(
            user=request.user, status="scheduled"
        )
        total_scheduled_payment = (
            scheduled_payments.aggregate(total=Sum("amount"))["total"] or 0
        )
        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "Scheduled payments retrieved successfully.",
                "data": SchedulePaymentSerializer(
                    scheduled_payments, many=True
                ).data,
                "total_scheduled_payment": total_scheduled_payment,
            },
        )

    @swagger_auto_schema(
        operation_description="Get wallet",
        operation_summary="Get wallet",
        tags=["Payment"],
    )
    @action(methods=["GET"], detail=False)
    def wallet(self, request):
        """
        Get wallet.
        """
        wallet = Wallet.objects.filter(user=request.user).first()
        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "Wallet retrieved successfully.",
                "data": WalletSerializer(wallet).data,
            },
        )

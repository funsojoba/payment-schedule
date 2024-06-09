import requests
from django.conf import settings

from django.db import transaction
from django.db.models import F

from django.contrib.auth import get_user_model

from payment.models import Wallet, Payment
from notification.service import EmailService


User = get_user_model()


class PayStack:
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    @classmethod
    def initiate_payment(cls, amount: int, email: str):
        """
        Make a payment
        """
        url = "{settings.PAYSTACK_BASE_URL}transaction/initialize"

        data = {"email": email, "amount": amount * 100}  # converting into Kobo

        response = requests.post(url, headers=cls.headers, json=data)
        response_data = response.json()

        if response.status_code == 200:
            return True, response_data["status"], response_data["data"]

        return False, response_data["status"], response_data["message"]

    def verify_transaction(cls, reference: dict):
        url = f"{settings.PAYSTACK_BASE_URL}transaction/verify/{reference}"
        response = requests.get(url, headers=cls.headers)
        response_data = response.json()

        if response.status_code == 200:
            return response_data["status"], response_data["data"]

        return response_data["status"], response_data["message"]


class PaymentUtil:

    def make_payment(cls, amount, email, currency="NGN"):
        user = User.objects.filter(email=email).first()

        with transaction.atomic():
            wallet = wallet = Wallet.objects.select_for_update().get(
                user=user, currency=currency
            )

            if wallet.total_amount < amount:
                EmailService.send_async(
                    template="insufficient_balance.html",
                    subject="Insufficient Balance",
                    recipients=[email],
                    context={
                        "name": user.display_name,
                        "currency": wallet.currency,
                        "amount": amount,
                    },
                )
                return False

            # Initiate Paystack
            status, intiated_payment = PayStack.initiate_payment(
                amount=amount, email=email
            )

            if not status:
                EmailService.send_async(
                    template="paystack_error.html",
                    subject="Payment Error",
                    recipients=[email],
                    context={
                        "name": user.display_name,
                        "currency": wallet.currency,
                        "amount": amount,
                    },
                )

            status, verify_payment = PayStack.verify_transaction(
                intiated_payment.get("reference")
            )

            # todo: Populate payment log
            if status:

                Payment.objects.create(
                    user=user,
                    amount=amount,
                    status="paid",
                    reference=verify_payment.get("reference"),
                    paystack_payment_id=verify_payment.get("id"),
                )

                wallet.total_amount = F("total_amount") - amount
                wallet.save()

                return True
            return False

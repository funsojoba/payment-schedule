import requests
from django.conf import settings




class PaymentUtil:

    @classmethod
    def make_payment(cls, amount, currency, user):
        """
        Make a payment
        """
        return requests.post(
            "http://localhost:8000/payment/",
            json={
                "amount": amount,
                "currency": currency,
                "email": user.email,
            },
            headers={
                "Authorization": f"Token {user.auth_token}"
            }
        )

from celery import shared_task
from notification.service import EmailService

from payment.models import ScheduledPayment
from payment.utils import PaymentUtil


@shared_task(bind=True)
def schedule_payment() -> None:
    all_scheduled_payment = ScheduledPayment.objects.filter(status="scheduled")

    for scheduled_payment in all_scheduled_payment:
        amount = scheduled_payment.amount
        email = scheduled_payment.user.email

        make_payment = PaymentUtil.make_payment(amount=amount, email=email)

        if make_payment:
            scheduled_payment.status = "fullfilled"
            schedule_payment.save()

            EmailService.send_async(
                template="payment_success.html",
                subject="Scheduled Payment Success",
                recipients=[email],
                context={
                    "name": scheduled_payment.user.display_name,
                    "amount": amount,
                    "currency": scheduled_payment.currency,
                    "description": scheduled_payment.description,
                },
            )

        else:
            EmailService.send_async(
                template="payment_fail.html",
                subject="Scheduled Payment Failed",
                recipients=[email],
                context={
                    "name": scheduled_payment.user.display_name,
                    "amount": amount,
                    "currency": scheduled_payment.currency,
                    "description": scheduled_payment.description,
                },
            )

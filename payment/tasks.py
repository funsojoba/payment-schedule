import smtplib
from typing import List, Dict
from celery import shared_task
from Notification.utils import EmailManager


@shared_task(
    bind=True,
)
def schedule_payment(
    self, 
):
    mail = EmailManager(
        template=template,
        recipients=recipients,
        subject=subject,
        context=context,
    )
    mail.send()

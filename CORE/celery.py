from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CORE.settings")

app = Celery("CORE")

# Configure Celery using settings from Django settings.py.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load tasks from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    "run-update-old-event-status-every-24-hours": {
        "task": "task.make-scheduled-payment",
        "schedule": crontab(day_of_week="0-6", hour=0, minute=00),
    }
}

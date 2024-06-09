# Generated by Django 4.2.13 on 2024-06-09 15:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0003_alter_payment_currency_scheduledpayment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="payment",
            name="schedule_date",
        ),
        migrations.AddField(
            model_name="payment",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="payment",
            name="paystack_payment_id",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name="payment",
            name="reference",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name="scheduledpayment",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="scheduledpayment",
            name="schedule_date",
            field=models.DateTimeField(verbose_name=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="scheduledpayment",
            name="status",
            field=models.CharField(
                choices=[
                    ("scheduled", "Scheduled"),
                    ("failed", "failed"),
                    ("fullfilled", "Fullfilled"),
                ],
                default="scheduled",
                max_length=10,
            ),
        ),
    ]
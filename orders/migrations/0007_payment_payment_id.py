# Generated by Django 4.2.7 on 2024-09-13 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_remove_order_status_order_payment_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(default=None, max_length=100, unique=True, verbose_name='شناسه پرداخت'),
        ),
    ]
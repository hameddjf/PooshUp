# Generated by Django 4.2.7 on 2024-09-14 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_remove_orderproduct_ordered'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='ordered',
            field=models.BooleanField(default=False, verbose_name='سفارش داده شده'),
        ),
    ]

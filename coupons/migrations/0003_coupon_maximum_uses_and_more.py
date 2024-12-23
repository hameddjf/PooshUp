# Generated by Django 4.2.7 on 2024-08-21 13:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0002_alter_coupon_coupon_validity_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='maximum_uses',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='coupon_validity_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]

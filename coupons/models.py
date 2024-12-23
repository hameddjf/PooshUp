from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from datetime import datetime, time
# Create your models here.


class Coupon(models.Model):
    COUPON_TYPE = (
        ('One Time', 'One Time'),
        ('With Time', 'With Time'),
        ('Permanent', 'Permanent'),
    )

    code = models.CharField(max_length=30, unique=True)
    discount_percent = models.PositiveSmallIntegerField(_("Discount Percent"))
    coupon_type = models.CharField(max_length=20, choices=COUPON_TYPE)
    coupon_validity_time = models.DateTimeField(
        null=True, blank=True, default=timezone.now)

    created_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    used_count = models.PositiveIntegerField(_("Used Count"), default=0)
    maximum_uses = models.PositiveIntegerField(default=1)

    def calculate_discount_amount(self, product_price):
        return product_price * (self.discount_percent / 100)

    def is_valid(self, order_status=None):
        """اعتبارسنجی کوپن بر اساس نوع و شرایط مختلف."""
        current_time = timezone.now()

        # اعتبارسنجی وضعیت فعلی
        if not self.is_active:
            return False
        if self.coupon_type == 'Permanent':
            return True
        elif self.coupon_type == 'With Time':
            return self.coupon_validity_time and self.coupon_validity_time > current_time
        elif self.coupon_type == 'One Time':
            return self.used_count < self.maximum_uses and (order_status == 'OnPay' or order_status is None)
        return False

    def increment_usage(self):
        """افزایش تعداد استفاده کوپن."""
        if self.used_count < self.maximum_uses:
            self.used_count += 1
            self.save()
        else:
            raise ValueError("این کوپن حداکثر تعداد استفاده را دارد.")

    def __str__(self):
        return f"{self.code} - {self.discount_percent}"

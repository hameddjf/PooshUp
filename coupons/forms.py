from django import forms
from .models import Coupon
from datetime import datetime, timedelta


class CouponApplyForm(forms.Form):
    coupon_code = forms.CharField(max_length=30, required=True)

    def test_coupon(self):
        # استفاده از datetime.now() به جای datetime.now().time()
        current_time = datetime.now()
        coupon = Coupon.objects.create(
            code='TESTCOUPON',
            discount_percent=10,
            coupon_type='Permanent',
            # تنظیم زمان انقضا به 1 ساعت بعد از زمان کنونی
            coupon_validity_time=current_time + timedelta(hours=1),
            used_count=0,
            is_active=True
        )
        return coupon

    def clean_coupon_code(self):
        coupon_code = self.cleaned_data['coupon_code']
        if coupon_code == 'TESTCOUPON':
            # متد را با self. فراخوانی کنید
            self.cleaned_data['coupon'] = self.test_coupon()
            return coupon_code
        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            if not coupon.is_valid(order_status='OnPay'):
                raise forms.ValidationError('کوپن نامعتبر است')
            self.cleaned_data['coupon'] = coupon
        except Coupon.DoesNotExist:
            raise forms.ValidationError('کوپن نامعتبر است')
        return coupon_code

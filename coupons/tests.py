from django.test import TestCase

# Create your tests here.
from datetime import datetime, timedelta


def test_coupon():
    # ایجاد یک کوپن معتبر
    coupon = Coupon.objects.create(
        code='TESTCOUPON',
        coupon_type='With Time',
        coupon_validity_time=datetime.now().time() + timedelta(hours=1),
        used_count=0,
        is_active=True
    )
    return coupon


def clean_coupon_code(self):
    coupon_code = self.cleaned_data['coupon_code']
    if coupon_code == 'TESTCOUPON':
        self.cleaned_data['coupon'] = test_coupon()
        return coupon_code
    try:
        coupon = Coupon.objects.get(code=coupon_code, is_active=True)
        if not coupon.is_valid(order_status='OnPay'):
            raise forms.ValidationError('کوپن نامعتبر است')
        self.cleaned_data['coupon'] = coupon
    except Coupon.DoesNotExist:
        raise forms.ValidationError('کوپن نامعتبر است')
    return coupon_code

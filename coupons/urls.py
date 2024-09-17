from django.urls import path
from .views import CouponApplyView

app_name = 'coupons'
urlpatterns = [
    path('apply-coupon/', CouponApplyView.as_view(), name='apply_coupon'),
]

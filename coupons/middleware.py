from django.contrib import messages
from .models import Coupon


# class CouponMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # بررسی وجود کد کوپن در سشن
#         coupon_code = request.session.get('coupon_code', None)
#         if coupon_code:
#             try:
#                 # دریافت کوپن از پایگاه داده بر اساس کد
#                 coupon = Coupon.objects.get(code=coupon_code)
#                 if coupon.is_valid(order_status='OnPay'):
#                     request.coupon = coupon
#                 else:
#                     del request.session['coupon_code']
#                     messages.error(request, 'کوپن نامعتبر است')
#                 # اضافه کردن کوپن به request
#                 request.coupon = coupon
#             except Coupon.DoesNotExist:
#                 # در صورت عدم وجود کوپن در پایگاه داده، حذف آن از سشن
#                 del request.session['coupon_code']
#                 messages.error(request, 'کوپن نامعتبر است')

#         response = self.get_response(request)
#         return response


class CouponMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # بررسی وجود سفارش و کوپن در سشن
        order = request.session.get('order')
        coupon_code = request.session.get('coupon_code')
        if order and coupon_code:
            try:
                # دریافت کوپن از پایگاه داده
                coupon = Coupon.objects.get(code=coupon_code)
                # request.coupon = coupon

                # حذف کوپن پس از ثبت سفارش
                coupon.delete()
                del request.session['coupon_code']
                messages.success(request, 'کوپن با موفقیت حذف شد.')
            except Coupon.DoesNotExist:
                pass

        return response

import json
from datetime import datetime

from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views import View

from .forms import CouponApplyForm
from .models import Coupon
from .templatetags.coupon_utils import OrderProductPriceCalculator

from carts.models import CartItem, Cart


class CouponApplyView(View):
    def get(self, request, *args, **kwargs):
        coupon_code = request.GET.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                if not coupon.is_valid(order_status='OnPay'):
                    response_data = {
                        'success': False,
                        'message': 'کوپن نامعتبر است.'
                    }
                else:
                    # Calculate total price with coupon
                    cart_items = CartItem.objects.filter(
                        user=request.user if request.user.is_authenticated else Cart.objects.get(
                            cart_id=_cart_id(request)).cartitem_set.all()
                    )
                    total_price_without_coupon = sum(
                        item.product.price * item.quantity for item in cart_items)
                    total_price_with_coupon = total_price_without_coupon * \
                        (1 - coupon.discount_percent / 100)
                    tax_amount = (2 * total_price_with_coupon) / 100

                    response_data = {
                        'success': True,
                        'coupon_code': coupon.code,
                        'discount_percent': coupon.discount_percent,
                        'total_price_without_coupon': total_price_without_coupon,
                        'total_price_with_coupon': total_price_with_coupon,
                        'tax_amount': tax_amount
                    }
            except Coupon.DoesNotExist:
                response_data = {
                    'success': False,
                    'message': 'کوپن نامعتبر است.'
                }
        else:
            response_data = {
                'success': False,
                'message': 'کد کوپن ارائه نشده است.'
            }
        return JsonResponse(response_data)

    def post(self, request, *args, **kwargs):
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            coupon = form.cleaned_data['coupon']

            # Retrieve cart items
            cart_items = CartItem.objects.filter(
                user=request.user if request.user.is_authenticated else Cart.objects.get(
                    cart_id=_cart_id(request)).cartitem_set.all()
            )

            # Calculate total price with coupon
            total_price_without_coupon = sum(
                item.product.discount_price * item.quantity if item.product.discount_price else
                item.product.price * item.quantity for item in cart_items
            )
            tax = (2 * total_price_without_coupon) / 100

            total_price_with_coupon = total_price_without_coupon * \
                (1 - coupon.discount_percent / 100) + \
                (2 * total_price_without_coupon) / 100
            tax_amount = (2 * total_price_with_coupon) / 100
            total = total_price_with_coupon + tax_amount

            # Save coupon and calculated values in session
            request.session['coupon_code'] = coupon.code
            request.session['discount_percent'] = coupon.discount_percent
            request.session['total_price_without_coupon'] = total_price_without_coupon
            request.session['total_price_with_coupon'] = total_price_with_coupon
            request.session['tax_amount'] = tax_amount
            request.session['total'] = total

            # Update cart total price
            cart = cart_items.first().cart if cart_items else None
            if cart:
                cart.total_price = total_price_with_coupon
                cart.save()

            return redirect('cart:checkout_page')
        else:
            return redirect('cart:cart_page')

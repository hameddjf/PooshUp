import logging
import json
import requests
from datetime import date, datetime

from django.urls import reverse
from django.http import HttpResponse, Http404, JsonResponse
from django.views import View
from django.utils import timezone
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import OrderForm
from .models import Order, OrderProduct, Payment

from coupons.models import Coupon
from carts.models import CartItem, Cart
from store.models import Product
from coupons.templatetags.coupon_utils import OrderProductPriceCalculator


from azbankgateways.exceptions import AZBankGatewaysException
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)

# Create your views here.


class PaymentView(View):
    def post(self, request):
        order = Order.objects.create(
            user=request.user,
            amount=request.POST.get('amount'),
            order_number=request.POST.get('order_number'),
            # سایر اطلاعات سفارش
        )
        amount = order.amount
        factory = bankfactories.BankFactory()
        try:
            bank = factory.auto_create()
            bank.set_request(request)
            bank.set_amount(amount)
            bank.set_client_callback_url(reverse('callback-gateway'))
            bank.set_mobile_number(request.user.phone_number)

            bank_record = bank.ready()

            if bank_record.is_success:
                order.bank_record = bank_record
                order.save()

                # ایجاد پرداخت
                payment = Payment.objects.create(
                    user=request.user,
                    order=order,
                    bank_record=bank_record
                )

                return bank.redirect_gateway()
            else:
                order.payment_status = 'failed'
                order.save()
                return HttpResponse("خطا در شروع فرآیند پرداخت.")

        except AZBankGatewaysException as e:
            order.payment_status = 'failed'
            order.save()
            logging.critical(str(e))
            return HttpResponse("خطا در شروع فرآیند پرداخت.")


class PaymentCallbackView(View):
    def get(self, request):
        tracking_code = request.GET.get(
            settings.TRACKING_CODE_QUERY_PARAM, None)
        if not tracking_code:
            return HttpResponse("لینک نامعتبر است.", status=404)

        try:
            bank_record = Bank.objects.get(tracking_code=tracking_code)
        except Bank.DoesNotExist:
            return HttpResponse("لینک نامعتبر است.", status=404)

        if bank_record.is_success:
            try:
                payment = Payment.objects.get(bank_record=bank_record)
                order = payment.order
                return redirect('order:order_complete_page', order_number=order.order_number, transID=bank_record.tracking_code)
            except Payment.DoesNotExist:
                logging.error("پرداخت مربوط به این رکورد بانکی یافت نشد.")
                return HttpResponse("پرداخت یافت نشد.", status=404)
        else:
            return HttpResponse("پرداخت ناموفق بود. اگر مبلغی کسر شده است، ظرف 48 ساعت بازگردانده خواهد شد.")


class GoToGatewayView(View):
    def get(self, request):
        # Read the amount from the PlaceOrderView
        order = Order.objects.filter(
            user=request.user, is_ordered=False).last()
        if order:
            amount = order.grand_total
        else:
            amount = 1000000

        user_mobile_number = "+9809931835803"

        factory = bankfactories.BankFactory()
        print('factory',factory)
        try:
            bank = factory.auto_create()
            print('bank1',bank)
            
            bank.set_request(request)

            # Set the amount to the calculated value
            bank.set_amount(amount)
            bank.set_client_callback_url(reverse('order:order_complete_page'))
            bank.set_mobile_number(user_mobile_number)
            print('bank2',bank)

            bank_record = bank.ready()
            print('bank_record',bank_record)
            
            order.bank_record = bank_record
            order.save()
            print('order',order)
            
            if settings.IS_SAFE_GET_GATEWAY_PAYMENT:
                context = bank.get_gateway()
                return render(request, "redirect_to_bank.html", context=context)
            else:
                return bank.redirect_gateway()
        except AZBankGatewaysException as e:
            logging.critical(f"AZBankGatewaysException: {e}")
            return self.handle_exception(e, request)
        except Exception as e:
            logging.critical(f"General Exception: {e}")
            return self.handle_exception(e, request)

        # Redirect the user to the order complete page
        return redirect('order:order_complete_page', order_number=order.order_number, transID=payment.payment_id)

    def handle_exception(self, exception, request):
        if settings.IS_SAFE_GET_GATEWAY_PAYMENT:
            return render(request, "redirect_to_bank.html", {'error': str(exception)})
        else:
            raise exception


# order_complete view
class OrderCompleteView(LoginRequiredMixin, View):
    login_url = 'account:login_page'

    def get(self, request):
        transID = request.GET.get('transID')

        try:
            payment = Payment.objects.get(bank_record__tracking_code=transID)
            order = payment.order

            # if payment.bank_record.is_success and payment.status != 'completed':
            #     # payment
            #     payment.status = 'completed'
            #     payment.save()

            #     # order
            #     order.is_ordered = True
            #     order.save()

            if order.user != request.user:
                return redirect('account:my_orders_page')

            ordered_products = OrderProduct.objects.filter(order_id=order.id)

            # محاسبه مجموع قیمت برای هر آیتم
            for item in ordered_products:
                item.total_price = item.product_price * item.quantity

            subtotal = sum(item.total_price for item in ordered_products)

            context = {
                'order': order,
                'ordered_products': ordered_products,
                'order_number': order.order_number,
                'transID': payment.bank_record.tracking_code,
                'payment': payment,
                'subtotal': subtotal,
                'bank_name': payment.bank_record.bank_type,
                'tracking_code': payment.bank_record.tracking_code,
                'amount': payment.bank_record.amount,
                'reference': payment.bank_record.reference_number,
                'bank_result': payment.bank_record.result,
                'callback_url': payment.bank_record.callback_url,
                'description': payment.bank_record.extra_information,
                'gateway_id': payment.bank_record.id,
                'created_at': payment.bank_record.created_at,
                'updated_at': payment.bank_record.updated_at,
            }
            return render(request, 'orders/order_complete.html', context)

        except Payment.DoesNotExist:
            logging.error(f"Payment not found for transID: {transID}")
            return redirect('account:my_orders_page')
        except Exception as e:
            logging.error(f"Error in OrderCompleteView: {str(e)}")
            return redirect('account:my_orders_page')


class PlaceOrderView(View):

    def get(self, request):
        current_user = request.user

        # if the cart count is less than or equal to 0, then redirect back to shop
        cart_items = CartItem.objects.filter(user=current_user)
        cart_count = cart_items.count()
        if cart_count <= 0:
            return redirect('store')
        for cart_item in cart_items:
            total += (cart_item.product.discount_price *
                      cart_item.quantity if cart_item.product.discount_price else cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total_price) / 100
        grand_total = total + tax
        order_total = total

        context = {
            'total_price': total,
            'quantity': cart_items.count(),
            'cart_items': cart_items,
            'tax': tax,
            'grand_total': total_price_with_coupon + tax,
            'order_total': total_price_with_coupon,
        }
        return render(request, 'orders/payments.html', context)

    def post(self, request):
        current_user = request.user
        cart_items = CartItem.objects.filter(user=current_user)
        total_price = self.calculate_total_price(cart_items)
        tax = (2 * total_price) / 100
        grand_total = total_price + tax
        order_total = total_price

        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.postal_code = form.cleaned_data['postal_code']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.street = form.cleaned_data['street']
            data.tag = form.cleaned_data['tag']
            data.order_total = total_price
            data.tax = tax
            data.grand_total = total_price + tax
            data.ip = request.META.get('REMOTE_ADDR',)
            data.save()

            # Generate order number
            order_number = self.generate_order_number(data)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total_price': order_total,
                'tax': tax,
                'grand_total': grand_total,
                'order_total': order_total,
            }
            return render(request, 'orders/payments.html', context,)
        else:
            return redirect('cart:checkout_page')

    def calculate_total_price(self, cart_items):
        total_price = 0
        for cart_item in cart_items:
            total_price += (cart_item.product.discount_price *
                            cart_item.quantity if cart_item.product.discount_price else cart_item.product.price * cart_item.quantity)
        return total_price

    def generate_order_number(self, data):
        yr = int(date.today().strftime('%Y'))
        dt = int(date.today().strftime('%d'))
        mt = int(date.today().strftime('%m'))
        d = date(yr, mt, dt)
        current_date = d.strftime('%Y%m%d')
        order_number = current_date + str(data.id)
        return order_number

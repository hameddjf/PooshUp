
import requests
import logging
import re

from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models.query_utils import Q
from django.views.generic import TemplateView
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


from .models import Cart, CartItem

from store.models import Product, Variation
from orders.forms import OrderForm
# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


class CartView(View):
    def get(self, request, product_id=None):
        try:
            tax = 0
            grand_total = 0
            total = 0
            quantity = 0
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(
                    user=request.user, is_active=True)
            else:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    cart_items = CartItem.objects.filter(
                        cart=cart, is_active=True)
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=_cart_id(request))
                    cart_items = []
            for cart_item in cart_items:
                total += (cart_item.product.discount_price *
                          cart_item.quantity if cart_item.product.discount_price else cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2 * total) / 100
            grand_total = total + tax

            context = {
                'total': total,
                'quantity': quantity,
                'cart_items': cart_items,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'store/cart.html', context)
        except Exception as e:
            # Log the exception or handle it in some other way
            print(f"Error in CartView.get: {e}")
            return render(request, 'store/cart.html', {
                'total': 0,
                'quantity': 0,
                'cart_items': [],
                'tax': 0,
                'grand_total': 0,
            })

    def post(self, request, product_id):
        current_user = request.user
        product = get_object_or_404(Product, pk=product_id)

        quantity = int(request.POST.get('quantity', 1))
        # if the user is authenticated
        if current_user.is_authenticated:
            product_variation = []
            if request.method == "POST":
                for item in request.POST:
                    try:
                        variation = Variation.objects.get(
                            variation_category__iexact=item,
                            variation_value__iexact=request.POST[item],
                            variation_products=product
                        )
                        product_variation.append(variation)
                    except Variation.DoesNotExist:
                        pass

            is_cart_item_exists = CartItem.objects.filter(
                product=product, user=current_user, variations__in=product_variation).exists()

            if is_cart_item_exists:
                cart_item = CartItem.objects.filter(
                    product=product, user=current_user, variations__in=product_variation)
                # existing variations --> database
                # current variations --> product_variation
                # item id --> database
                existing_variation_list = []
                id = []
                for item in cart_item:
                    existing_variation = item.variations.all()
                    existing_variation_list.append(list(existing_variation))
                    id.append(item.id)

                if product_variation in existing_variation_list:
                    # increase cart item quantity
                    index = existing_variation_list.index(product_variation)
                    item_id = id[index]
                    item = CartItem.objects.get(id=item_id)
                    item.quantity += quantity
                    item.save()
                else:
                    cart_item = CartItem.objects.get(
                        product=product, user=current_user, variations__in=product_variation)
                    cart_item.variations.set(product_variation)
                    cart_item.quantity += quantity
                    cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    quantity=quantity,
                    user=current_user,
                )
                cart_item.variations.set(product_variation)
                cart_item.save()
            return redirect('cart:cart_page')
        # if user is not authenticated
        else:
            product_variation = []
            if request.method == "POST":
                for item in request.POST:
                    try:
                        variation = Variation.objects.get(
                            variation_category__iexact=item,
                            variation_value__iexact=request.POST[item],
                            variation_products=product
                        )
                        product_variation.append(variation)
                    except Variation.DoesNotExist:
                        pass

            try:
                # get the cart using the cart_id present in the session
                cart = Cart.objects.get(cart_id=self._cart_id(request))
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id=self._cart_id(request)
                )
            cart.save()
            is_cart_item_exists = CartItem.objects.filter(
                product=product, cart=cart, variations__in=product_variation).exists()

            if is_cart_item_exists:
                cart_item = CartItem.objects.filter(
                    product=product, cart=cart, variations__in=product_variation)
                # existing variations --> database
                # current variations --> product_variation
                # item id --> database
                existing_variation_list = []
                id = []
                for item in cart_item:
                    existing_variation = item.variations.all()
                    existing_variation_list.append(list(existing_variation))
                    id.append(item.id)

                if product_variation in existing_variation_list:
                    # increase cart item quantity
                    index = existing_variation_list.index(product_variation)
                    item_id = id[index]
                    item = CartItem.objects.get(id=item_id)
                    item.quantity += 1
                    item.save()
                else:
                    cart_item = CartItem.objects.get(
                        product=product, cart=cart, variations__in=product_variation)
                    cart_item.variations.set(product_variation)
                    cart_item.quantity += 1
                    cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    quantity=1,
                    cart=cart,
                )
                cart_item.variations.set(product_variation)
                cart_item.save()
            return redirect('cart:cart_page')


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except Cart.DoesNotExist:
        pass
    return redirect('cart:cart_page')


def delete_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(
            product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(
            product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart:cart_page')


@method_decorator(login_required(login_url='account:login_page'), name='dispatch')
class CheckoutView(TemplateView):
    template_name = 'store/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get states from the API
        states_response = requests.get(
            "https://iran-locations-api.ir/api/v1/fa/states")
        states = states_response.json()
        context['states'] = states

        # Get cities based on selected state
        if 'state' in self.request.GET:
            state_name = self.request.GET.get('state')
            cities_response = requests.get(
                f"https://iran-locations-api.ir/api/v1/fa/cities?state={state_name}")
            cities = cities_response.json()
            logging.info(f"Cities: {cities}")
        elif 'state_id' in self.request.GET:
            state_id = self.request.GET.get('state_id')
            cities_response = requests.get(
                f"https://iran-locations-api.ir/api/v1/fa/cities?state_id={state_id}")
            cities = cities_response.json()
            logging.info(f"Cities: {cities}")
        else:
            cities = []
            logging.info(f"Cities: {cities}")
        context['cities'] = cities
        try:
            total = 0
            quantity = 0
            if self.request.user.is_authenticated:
                cart_items = CartItem.objects.filter(
                    user=self.request.user, is_active=True)
            else:
                cart = Cart.objects.get(cart_id=self._cart_id(self.request))
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2 * total) / 100
            grand_total = total + tax
            context.update({
                'total': total,
                'quantity': quantity,
                'cart_items': cart_items,
                'tax': tax,
                'grand_total': grand_total,
            })
        except ObjectDoesNotExist:
            context['cart_items'] = []
        return context

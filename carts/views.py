from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views import View

from .models import Cart, CartItem

from store.models import Product, Variation
# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


class CartView(View):

    def get(self, request):
        try:
            tax = 0
            grand_total = 0
            total = 0
            quantity = 0
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(
                    user=request.user, is_active=True)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2 * total) / 100
            grand_total = total + tax
        except ObjectDoesNotExist:
            cart_items = []

        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'tax': tax,
            'grand_total': grand_total,
        }
        return render(request, 'store/cart.html', context)

    def post(self, request, product_id):
        current_user = request.user
        product = get_object_or_404(Product, pk=product_id)
        quantity = request.POST.get('quantity')
        if quantity is not None:
            quantity = int(quantity)
        else:
            quantity = 1

        # Ensure the quantity does not exceed the available stock
        if quantity > product.stock:
            quantity = product.stock

        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                if item in ['color', 'size']:
                    value = request.POST[item]
                    try:
                        variation = Variation.objects.get(
                            variation_category__iexact=item, variation_value__iexact=value)
                        product_variation.append(variation)
                    except Variation.DoesNotExist:
                        pass

        # If the user is authenticated
        if current_user.is_authenticated:
            cart_items = CartItem.objects.filter(
                product=product, user=current_user)
            if cart_items.exists():
                cart_item = cart_items.first()
                cart_item.quantity += quantity
                if cart_item.quantity > product.stock:
                    cart_item.quantity = product.stock
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    user=current_user,
                    product=product,
                    quantity=quantity
                )
                cart_item.save()
        # If the user is not authenticated
        else:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id=_cart_id(request)
                )
            cart.save()

            cart_items = CartItem.objects.filter(
                product=product, cart=cart)
            if cart_items.exists():
                cart_item = cart_items.first()
                cart_item.quantity += quantity
                if cart_item.quantity > product.stock:
                    cart_item.quantity = product.stock
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=quantity
                )
                cart_item.save()

        return redirect('cart:cart_page')
# private function


# def _cart_id(request):
#     cart = request.session.session_key
#     if not cart:
#         cart = request.session.create()
#     return cart


# def add_cart(request, product_id):
#     current_user = request.user
#     product = Product.objects.get(id=product_id)
#     # if the user is authenticated
#     if current_user.is_authenticated:
#         product_variation = []
#         if request.method == "POST":
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]

#                 try:
#                     variation = Variation.objects.get(
#                         product=product, variation_category__iexact=key,
#                         variation_value__iexact=value)
#                     product_variation.append(variation)
#                 except Variation.DoesNotExist:
#                     pass
#         is_cart_item_exists = CartItem.objects.filter(
#             product=product, user=current_user).exists()

#         if is_cart_item_exists:
#             cart_item = CartItem.objects.filter(
#                 product=product, user=current_user)
#             # exsisting variations --> database
#             # current variations --> product_varations
#             # item id --> database
#             existing_variation_list = []
#             id = []
#             for item in cart_item:
#                 existing_variation = item.variations.all()
#                 existing_variation_list.append(list(existing_variation))
#                 id.append(item.id)

#             if product_variation in existing_variation_list:
#                 # increase cart item quantity
#                 index = existing_variation_list.index(product_variation)
#                 item_id = id[index]
#                 item = CartItem.objects.get(product=product, id=item_id)
#                 item.quantity += 1
#                 item.save()
#             else:
#                 item = CartItem.objects.create(
#                     product=product, quantity=1, user=current_user)
#                 if len(product_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*product_variation)
#                 item.save()
#         else:
#             cart_item = CartItem.objects.create(
#                 product=product,
#                 quantity=1,
#                 user=current_user,
#             )
#             if len(product_variation) > 0:
#                 cart_item.variations.clear()
#                 cart_item.variations.add(*product_variation)
#             cart_item.save()
#         return redirect('cart:cart_page')
#     # if user is not authenticated
#     else:
#         product_variation = []
#         if request.method == "POST":
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]

#                 try:
#                     variation = Variation.objects.get(
#                         product=product, variation_category__iexact=key,
#                         variation_value__iexact=value)
#                     product_variation.append(variation)
#                 except Variation.DoesNotExist:
#                     pass

#         try:
#             # get the cart using the cart_id present in the session
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#         except Cart.DoesNotExist:
#             cart = Cart.objects.create(
#                 cart_id=_cart_id(request)
#             )
#         cart.save()
#         is_cart_item_exists = CartItem.objects.filter(
#             product=product, cart=cart).exists()

#         if is_cart_item_exists:
#             cart_item = CartItem.objects.filter(product=product, cart=cart)
#             # exsisting variations --> database
#             # current variations --> product_varations
#             # item id --> database
#             existing_variation_list = []
#             id = []
#             for item in cart_item:
#                 existing_variation = item.variations.all()
#                 existing_variation_list.append(list(existing_variation))
#                 id.append(item.id)
#             print(existing_variation_list)

#             if product_variation in existing_variation_list:
#                 # increase cart item quantity
#                 index = existing_variation_list.index(product_variation)
#                 item_id = id[index]
#                 item = CartItem.objects.get(product=product, id=item_id)
#                 item.quantity += 1
#                 item.save()
#             else:
#                 item = CartItem.objects.create(
#                     product=product, quantity=1, cart=cart)
#                 if len(product_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*product_variation)
#                 item.save()
#         else:
#             cart_item = CartItem.objects.create(
#                 product=product,
#                 quantity=1,
#                 cart=cart,
#             )
#             if len(product_variation) > 0:
#                 cart_item.variations.clear()
#                 cart_item.variations.add(*product_variation)
#             cart_item.save()
#         return redirect('cart:cart_page')


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


# def cart(request, total=0, quantity=0, cart_items=None):
#     try:
#         tax = 0
#         grand_total = 0
#         if request.user.is_authenticated:
#             cart_items = CartItem.objects.filter(
#                 user=request.user, is_active=True)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             total += (cart_item.product.price * cart_item.quantity)
#             quantity += cart_item.quantity
#         tax = (2 * total)/100
#         grand_total = total + tax
#     except ObjectDoesNotExist:
#         cart_items = []  # تعیین مقدار پیش‌فرض برای cart_items

#     context = {
#         'total': total,
#         'quantity': quantity,
#         'cart_items': cart_items,
#         'tax': tax,
#         'grand_total': grand_total,
#     }
#     return render(request, 'store/cart.html', context)


@login_required(login_url='account:login_page')
def checkout(request,  total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        cart_items = []  # تعیین مقدار پیش‌فرض برای cart_items

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)

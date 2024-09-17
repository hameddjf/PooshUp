import requests

from django.contrib import messages, auth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage

from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile

from carts.models import Cart, CartItem
from carts.views import _cart_id
from orders.models import Order, OrderProduct, Payment

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # user valid
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            # confirm_password = form.cleaned_data['confirm_password']

            user = Account.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            user.phone_number = phone_number
            user.save()

            # user activision
            curent_site = get_current_site(request)
            mail_subject = 'لطفا اکانتتان را فعال کنید .'
            message = render_to_string(
                'accounts/account_verification_email.html',
                {
                    'user': user,
                    'domain': curent_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return redirect('/accounts/login/?command-verification&email='
                            + email)
        else:
            # Form is not valid
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(
                    cart=cart,).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart,)

                    # getting the product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    # get cart items from user to access his product variations
                    cart_item = CartItem.objects.filter(
                        user=user)
                    # exsisting variations --> database
                    # current variations --> product_varations
                    # item id --> database
                    existing_variation_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        existing_variation_list.append(
                            list(existing_variation))
                        id.append(item.id)
                    for product in product_variation:
                        if product in existing_variation_list:
                            index = existing_variation_list.index(product)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except Cart.DoesNotExist:
                pass
            auth.login(request, user)
            # messages.success(request , 'شما وارد شدید .')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except ValueError:
                return redirect('account:profile_page')

        else:
            messages.error(request, 'رمز عبور خود را بازنشانی کنید .')
            return redirect('account:login_page')

    return render(request, 'accounts/login.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'تبریک ! حساب شما با موفقیت تایید شد .')
        return redirect('account:login_page')
    else:
        messages.error(request, 'لینک فعالسازی نامعتبر است .')
        return redirect('account:register_page')


@login_required(login_url='account:login_page')
def logout(request):
    auth.logout(request)
    messages.success(request, 'شما خارج شدید .')
    return redirect('account:login_page')


@login_required(login_url='account:login_page')
def profile(request):
    orders = Order.objects.filter(
        user_id=request.user.id, is_ordered=True).order_by('-created_at')
    orders_count = orders.count()

    try:
        userprofile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        userprofile = None

    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/profile.html', context)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        # check the email for existing in db (exact email or not)
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)

            # reset password email
            curent_site = get_current_site(request)
            mail_subject = 'لطفا اکانتتان را تایید کنید\
                برای تغییر رمز عبورتان .'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': curent_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(
                request, 'بازنشانی رمز عبور به ادرس ایمیلتان ارسال شد .')
            return redirect('account:login_page')
        else:
            messages.error(request, 'اکانت مورد نظر وجود ندارد .')
            return redirect('account:forgot_password_page')
    return render(request, 'accounts/forgot_password_checks.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'لطفا رمز عبور خودتان را بازنشانی کنید .')
        return redirect('account:reset_password_page')
    else:
        messages.error(request, 'این لینک منقضی شده است .')
        return redirect('account:login_page')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'با موفقیت رمز عبور باز نشانی شد .')
            return redirect('account:login_page')
        else:
            messages.error(request, 'رمز عبور مطابقت ندارد .')
            return redirect('account:reset_password_page')
    else:
        return render(request, 'accounts/password-update.html')


class MyOrdersView(LoginRequiredMixin, ListView):
    template_name = 'accounts/my_orders.html'
    context_object_name = 'orders_data'
    login_url = 'account:login_page'

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.filter(
            user=user, is_ordered=True).order_by('-created_at')
        orders_data = self.get_orders_data(orders)
        return orders_data

    def get_orders_data(self, orders):
        orders_data = []
        for order in orders:
            order_products = OrderProduct.objects.filter(order=order)
            payment = Payment.objects.filter(order=order).first()
            order_data = {
                'order': order,
                'order_products': order_products,
                'payment': payment,
            }
            orders_data.append(order_data)
        return orders_data


@login_required(login_url='account:login_page')
def edit_profile(request):
    userprofile, created = UserProfile.objects.get_or_create(
        user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'مشخصات شما به روز شده است.')
            return redirect('account:edit_profile_page')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='account:login_page')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'رمز عبور با موفقیت به روز شد.')
                return redirect('account:change_password_page')
            else:
                messages.error(
                    request, 'لطفا رمز عبور فعلی معتبر را وارد کنید')
                return redirect('account:change_password_page')
        else:
            messages.error(request, 'رمز عبور مطابقت ندارد!')
            return redirect('account:change_password_page')
    return render(request, 'accounts/change_password.html')


@login_required(login_url='account:login_page')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)

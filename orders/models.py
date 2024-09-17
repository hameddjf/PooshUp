from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from azbankgateways.models import Bank

# Create your models here.


class Payment(models.Model):

    bank_record = models.OneToOneField(
        Bank, on_delete=models.CASCADE, verbose_name=_("رکورد بانکی"), default=None)
    user = models.ForeignKey(
        "accounts.Account", on_delete=models.CASCADE, verbose_name=_("کاربر"))
    order = models.OneToOneField(
        "Order", on_delete=models.CASCADE, related_name="payment", default=None)
    status = models.CharField(_("وضعیت"), max_length=20, choices=[
        ('pending', 'در انتظار'),
        ('completed', 'کامل شده'),
        ('failed', 'ناموفق'),
    ], default='pending')

    created_at = models.DateTimeField(_("زمان ایجاد"), auto_now_add=True)

    class Meta:
        verbose_name = _("پرداختی")
        verbose_name_plural = _("پرداخت ها")

    def __str__(self):
        return f"Payment for order {self.order.order_number}"

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

    def get_status(self):
        return "Completed" if self.bank_record.is_success else "Failed"


class Order(models.Model):
    user = models.ForeignKey(
        "accounts.Account", verbose_name=_(
            "کاربر"), on_delete=models.SET_NULL, null=True)
    bank_record = models.OneToOneField(
        Bank, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("رکورد بانکی"), default=None)
    order_number = models.CharField(_("شماره سفارش "), max_length=20)
    first_name = models.CharField(_("نام "), max_length=50)
    last_name = models.CharField(_(" نام خوانوادگی"), max_length=50)
    phone = models.CharField(_(" شماره تماس"), max_length=11)
    email = models.EmailField(_(" ایمیل"), max_length=50)
    address_line_1 = models.CharField(_(" ادرس تحویل"), max_length=50)
    postal_code = models.CharField(_(" کد پستی"), max_length=50)
    state = models.CharField(_(" استان"), max_length=50)
    city = models.CharField(_("شهر "), max_length=50)
    street = models.CharField(_("خیابان "), max_length=50)
    tag = models.CharField(_(" پلاک"), max_length=50)
    order_total = models.IntegerField(_(" قیمت کل سفارشات"),)
    tax = models.IntegerField(_(" مالیات"),)
    grand_total = models.IntegerField(_("مجموع کل"), default=0)

    payment_status = models.CharField(_("وضعیت پرداخت"), max_length=20, choices=[
        ('pending', 'در انتظار پرداخت'),
        ('completed', 'پرداخت شده'),
        ('failed', 'ناموفق'),
    ], default='pending')
    ip = models.CharField(_(" ایپی"), blank=True, max_length=20)
    is_ordered = models.BooleanField(_(" سفارش داده شده"), default=False)
    created_at = models.DateTimeField(_("زمان ایجاد "), auto_now_add=True)
    updated_at = models.DateTimeField(_(" زمان بروزرسانی"), auto_now=True)

    def __str__(self):
        return self.order_number

    def get_payment_status(self):
        if self.bank_record:
            return "Completed" if self.bank_record.is_success else "Failed"
        return "Pending"

    def get_order_details(self):
        order_products = self.orderproduct_set.all()
        details = []
        for op in order_products:
            for product in op.product.all():
                details.append({
                    'name': product.product_name,
                    'price': product.price,
                    'quantity': op.quantity,
                    'total': product.price * op.quantity,
                    'variations': ', '.join([str(v) for v in op.variation.all()])
                })
        return details

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = _("سفارش ")
        verbose_name_plural = _("سفارشات")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, verbose_name=_(
        "سفارش"), on_delete=models.CASCADE)
    bank_record = models.OneToOneField(
        Bank, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("رکورد بانکی"), default=None)
    # payment = models.ForeignKey(
    #     Payment, verbose_name=_(
    #         "پرداختی"), on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey("accounts.Account", verbose_name=_(
        "کاربر"), on_delete=models.CASCADE)
    product = models.ForeignKey("store.Product", verbose_name=_(
        "محصول"), on_delete=models.CASCADE)
    variation = models.ManyToManyField("store.Variation",
                                       verbose_name=_("واریانت"),
                                       blank=True)
    payment_status = models.CharField(_("وضعیت پرداخت"), max_length=20, choices=[
        ('pending', 'در انتظار پرداخت'),
        ('completed', 'پرداخت شده'),
        ('failed', 'ناموفق'),
    ], default='pending')
    ordered = models.BooleanField(_("سفارش داده شده"), default=False)
    quantity = models.IntegerField(_(" تعداد"),)
    created_at = models.DateTimeField(_(" زمان ایجاد"), auto_now_add=True)
    updated_at = models.DateTimeField(_(" زمان بروزرسانی"), auto_now=True)

    coupon = models.ForeignKey(
        'coupons.Coupon', on_delete=models.CASCADE, related_name='orderproduct_coupons', null=True, blank=True, default=None
    )

    @property
    def is_ordered(self):
        return self.order.payment_status == 'completed'

    @property
    def total_price_with_discount(self):
        return self.product.discount_price * self.quantity

    @property
    def total_price_with_coupon(self):
        return self.calc_price_with_coupon()

    def calc_price_with_coupon(self):
        total_price_with_discount = self.total_price_with_discount
        if self.coupon:
            discount_amount = self.coupon.calculate_discount_amount(
                total_price_with_discount)
            total_price_with_coupon = total_price_with_discount - discount_amount
        else:
            total_price_with_coupon = total_price_with_discount
        tax = (2 * total_price_with_coupon) / 100
        return total_price_with_coupon + tax

    def apply_coupon(self, coupon, total_price_with_discount):
        if coupon.is_valid(order_status='OnPay'):
            discount_amount = coupon.calculate_discount_amount(
                total_price_with_discount)
            return total_price_with_discount - discount_amount
        else:
            return total_price_with_discount

    class Meta:
        verbose_name = _("سفارش محصول")
        verbose_name_plural = _("سفارش محصولات")

    def __str__(self):
        return str(self.user)

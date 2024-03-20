from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey("accounts.Account", verbose_name=_(
        "کاربر"), on_delete=models.CASCADE)
    payment_id = models.CharField(_("ایدی سفارش"), max_length=100)
    payment_method = models.CharField(_("روش پرداخت"), max_length=100)
    amount_paid = models.CharField(
        _("مقدار پرداختی"), max_length=100)  # this is total amount paid
    status = models.CharField(_("وضعیت"), max_length=100)
    created_at = models.DateTimeField(_("زمان ایجاد"), auto_now_add=False)

    class Meta:
        verbose_name = _("پرداختی")
        verbose_name_plural = _("پرداخت ها")

    def __str__(self):
        return self.payment_id

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Order(models.Model):
    STATUS = (
        ('new', 'جدید'),
        ('accepted', 'پذیرفته شده'),
        ('completed', 'کامل شده'),
        ('cancelled', 'لغو شده'),
    )
    user = models.ForeignKey(
        "accounts.Account", verbose_name=_(
            "کاربر"), on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(
        Payment, verbose_name=_(
            "پرداختی"), on_delete=models.SET_NULL, blank=True, null=True)
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
    # order_note = models.CharField(_(" "),max_length=50)
    order_total = models.FloatField(_(" تمام سفارشات"),)
    tax = models.FloatField(_(" مالیات"),)
    status = models.CharField(_(" وضعیت"), max_length=10,
                              choices=STATUS, default='New')
    ip = models.CharField(_(" ایپی"), blank=True, max_length=20)
    is_ordered = models.BooleanField(_(" سفارش داده شده"), default=False)
    created_at = models.DateTimeField(_("زمان ایجاد "), auto_now_add=True)
    updated_at = models.DateTimeField(_(" زمان بروزرسانی"), auto_now=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1}'

    class Meta:
        verbose_name = _("سفارش")
        verbose_name_plural = _("سفارش ها")

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, verbose_name=_(
        "سفارش"), on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, verbose_name=_(
            "پرداختی"), on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey("accounts.Account", verbose_name=_(
        "کاربر"), on_delete=models.CASCADE)
    product = models.ForeignKey("store.Product", verbose_name=_(
        "محصول"), on_delete=models.CASCADE)
    variation = models.ForeignKey("store.Variation", verbose_name=_(
        "واریانت"), on_delete=models.CASCADE, blank=True)
    # color = models.CharField(_(" رنگ"), max_length=50)
    # size = models.CharField(_(" اندازه"), max_length=50)
    quantity = models.IntegerField(_(" تعداد"),)
    product_price = models.FloatField(_(" قیمت محصول"),)
    ordered = models.BooleanField(_(" سفارش داده شده"), default=False)
    created_at = models.DateTimeField(_(" زمان ایجاد"), auto_now_add=True)
    updated_at = models.DateTimeField(_(" زمان بروزرسانی"), auto_now=True)

    class Meta:
        verbose_name = _("سفارش محصول")
        verbose_name_plural = _("سفارش محصولات")

    def __str__(self):
        return self.first_name

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


# Create your models here.
class Category(models.Model):
    parent = models.ForeignKey(
        "self",
        verbose_name=_("دسته بندی"),
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )
    title = models.CharField(_("عنوان دسته بندی"), max_length=50)
    slug = models.SlugField(_("آدرس دسته بندی"), unique=True, max_length=50)
    description = models.TextField(_("توضیحات دسته بندی"), max_length=255)
    category_image = models.ImageField(
        _("تصویر دسته بندی"),
        upload_to='images/category_images',
        blank=True
    )

    class Meta:
        verbose_name = _("دسته بندی")
        verbose_name_plural = _("دسته بندی ها")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("products_by_category", args=[self.slug])


class Product(models.Model):
    COLOR_CHOICES = (
        ('ابی', 'ابی'),
        ('قرمز', 'قرمز'),
        ('زرد', 'زرد'),
        ('سیاه', 'سیاه'),
        ('سفید', 'سفید'),
        ('قهوه ای', 'قهوه ای'),
    )

    SIZE_CHOICES = (
        ('XL', 'XL'),
        ('S', 'S'),
        ('M', 'M'),
        ('XXL', 'XXL'),
        ('XXXL', 'XXXL'),
    )

    product_name = models.CharField(
        _("نام محصول"), max_length=255, unique=True)
    slug = models.SlugField(_("آدرس محصول"), unique=True)
    description = models.TextField(_("توضیحات کامل محصول"), max_length=550)
    information = models.CharField(_("توضیحات کوتاه"), max_length=255)
    concise = models.TextField(_("توضیح مختصر"), max_length=100)
    color = models.CharField(_("رنگ"), max_length=50, choices=COLOR_CHOICES)
    size = models.CharField(_("اندازه"), max_length=50, choices=SIZE_CHOICES)
    price = models.DecimalField(_("قیمت"), max_digits=11, decimal_places=2)
    image = models.ImageField(_("عکس"), upload_to='images/product_images')
    stock = models.IntegerField(_("موجودی"), default=0)
    discount = models.DecimalField(
        _("تخفیف"), max_digits=10, decimal_places=2, default=0)
    is_available = models.BooleanField(default=False)
    category = models.ForeignKey("core.Category", verbose_name=_(
        "دسته بندی"), on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("محصول")
        verbose_name_plural = _("محصولات")

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('products_detail', args=[self.category.slug, self.slug])

    @property
    def discount_price(self):
        return self.price * (1 - (self.discount / 100))

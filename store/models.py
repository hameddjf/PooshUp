from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from category.models import Category

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    concise = models.TextField(max_length=500, blank=True)
    description = models.TextField(max_length=500, blank=True)
    information = models.TextField(max_length=500, blank=True)
    color = models.CharField(max_length=55, default='سفید')
    size = models.CharField(max_length=55, default='بزرگ')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/product_images',
                              height_field=None,
                              width_field=None,
                              max_length=None)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, verbose_name='دسته بندی', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now=False, auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def discount_price(self):
        return self.price * (1-(self.discount / 100))

    def get_url(self):
        return reverse('products_detail', args=[self.category.slug, self.slug])

    class Meta:
        verbose_name = ("محصول")
        verbose_name_plural = ("محصولات")

    def __str__(self):
        return self.title


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, verbose_name=_(
        "محصول"), on_delete=models.CASCADE)
    variation_category = models.CharField(
        _("تنوع دسته بندی"), max_length=120, choices=variation_category_choice)
    variation_value = models.CharField(_("مقدار تنوع"), max_length=120)
    is_active = models.BooleanField(_("فعال است؟"), default=True)
    create_date = models.DateTimeField(
        _("زمان ایجاد"), auto_now=True, auto_now_add=False)

    objects = VariationManager()

    class Meta:
        verbose_name = ("واریانت")
        verbose_name_plural = ("واریانت ها")

    def __str__(self):
        return str(self.product)

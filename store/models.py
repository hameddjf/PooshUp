from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg, Count

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

    def averageReview(self):
        reviews = ReviewRating.objects.filter(
            product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
            avg_rounded = round(avg, 2)
        return avg_rounded

    def countReview(self):
        reviews = ReviewRating.objects.filter(
            product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

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
        return super(VariationManager, self).filter(variation_category='color',
                                                    is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size',
                                                    is_active=True)


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


class ReviewRating(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("محصول")
    )
    user = models.ForeignKey('accounts.Account',
                             on_delete=models.CASCADE, verbose_name=_("کاربر"))
    subject = models.CharField(_("موضوع"), max_length=100, blank=True)
    review = models.TextField(_("متن نظر"), max_length=500, blank=True)
    rating = models.FloatField(_("امتیاز"),)
    ip = models.CharField(_("ایپی"), max_length=20, blank=True)
    status = models.BooleanField(_("وضعیت"), default=True)
    created_at = models.DateTimeField(_("زمان ایجاد"), auto_now_add=True)
    updated_at = models.DateTimeField(_("زمان بروزرسانی"), auto_now_add=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = ("بررسی امتیاز")
        verbose_name_plural = ("بررسی امتیازات")


class ProductGallery(models.Model):
    Product = models.ForeignKey(
        Product, verbose_name=_("محصول"),
        on_delete=models.CASCADE)
    image = models.ImageField(
        _("عکس"), upload_to='store/products', max_length=255)

    def __str__(self):
        return self.Product.title

    class Meta:
        verbose_name = _("گالری محصول")
        verbose_name_plural = _("گالری محصولات")

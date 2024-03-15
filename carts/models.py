from django.db import models
from django.utils.translation import gettext_lazy as _

from store.models import Product, Variation
# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = ("کالا")
        verbose_name_plural = ("کالاها")

    def __str__(self):
        return self.cart_id

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,    on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    variations = models.ManyToManyField(
        Variation, verbose_name=_("واریانت ها"), blank=True)

    def sub_total(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = ("کالا سبد خرید")
        verbose_name_plural = ("کالاهای سبد خرید")

    def __str__(self):
        return str(self.product)

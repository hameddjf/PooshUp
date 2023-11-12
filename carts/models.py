from django.db import models
from store.models import Product
# Create your models here.

class Cart(models.Model):
    cart_id    = models.CharField(max_length=250 , blank = True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name        = ("کالا")
        verbose_name_plural = ("کالاها")

    def __str__(self):
        return self.cart_id

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})

class CartItem(models.Model):
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart      = models.ForeignKey(Cart,    on_delete=models.CASCADE)
    quantity  = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name        = ("کالا سبد خرید")
        verbose_name_plural = ("کالاهای سبد خرید")

    def __str__(self):
        return self.product

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})
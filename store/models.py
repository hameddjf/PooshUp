from django.db import models
from category.models import Category

# Create your models here.
class Product(models.Model):
    title           = models.CharField(max_length=50 ,unique = True)
    slug            = models.SlugField(max_length = 50 , unique = True)
    description     = models.TextField(max_length = 500 , blank = True)
    price           = models.DecimalField(max_digits=10, decimal_places=2)
    image           = models.ImageField(upload_to='images/product_images', height_field=None, width_field=None, max_length=None)
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default = False)
    category        = models.ForeignKey(Category, verbose_name='دسته بندی', on_delete=models.CASCADE)
    created_date    = models.DateField(auto_now=False, auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True, auto_now_add=False)
    discount        = models.DecimalField(max_digits=10, decimal_places=2 , default=0)

    @property
    def discount_price(self):
        return self.price *(1-(self.discount / 100))

    

    class Meta:
        verbose_name = ("محصول")
        verbose_name_plural = ("محصولات")

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})

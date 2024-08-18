from django.db import models
from django.urls import reverse


class Category(models.Model):
    product = models.ManyToManyField(
        "store.Product", related_name='product_category')
    parent = models.ForeignKey('self', default=None, null=True, blank=True,
                               on_delete=models.SET_NULL,
                               related_name='children',
                               verbose_name='دسته اصلی')
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=150)
    description = models.TextField(max_length=300, blank=True)
    category_image = models.ImageField(
        upload_to='images/category_images', blank=True)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def get_absolute_url(self):
        return reverse('products_by_category', args=[self.slug])

    def get_all_subcategories(self):
        all_subcategories = [self]
        if self.children.exists():
            for child in self.children.all():
                all_subcategories.extend(child.get_all_subcategories())
        return all_subcategories

    def __str__(self):
        return self.title

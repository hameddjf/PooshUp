from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True,
                               on_delete=models.SET_NULL, related_name='children', verbose_name='دسته اصلی')
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True , max_length=150)
    description = models.TextField(max_length=300 , blank=True)
    category_image = models.ImageField(upload_to='images/category_images' , blank = True)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def get_absolute_url(self):
        return reverse("products_by_category", args=[self.slug])
    


    def __str__(self):
        return self.title
    
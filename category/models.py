from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True , max_length=150)
    description = models.TextField(max_length=300 , blank=True)
    category_image = models.ImageField(upload_to='images/category_images' , blank = True)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


    def __str__(self):
        return self.title
    
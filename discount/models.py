from django.db import models
from django.utils import timezone


class Discount(models.Model):
    title = models.CharField(max_length=100)
    discount_percentage = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField(
        'store.Product', blank=True, related_name='discounts')
    category = models.ForeignKey(
        'category.Category', on_delete=models.SET_NULL, null=True, blank=True)
    # brand = models.ForeignKey('store.Brand', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def is_valid(self):
        return self.start_date <= timezone.now().date() <= self.end_date and self.is_active

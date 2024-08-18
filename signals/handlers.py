from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from store.models import Product
from category.models import Category


@receiver(post_save, sender=Product)
def update_category_products(sender, instance, created, **kwargs):
    if created:
        instance.category.products.add(instance)
    else:
        old_category = instance.category
        new_category = kwargs.get('update_fields', {}).get('category')
        if old_category != new_category:
            old_category.products.remove(instance)
            new_category.products.add(instance)


@receiver(post_delete, sender=Product)
def remove_product_from_category(sender, instance, **kwargs):
    instance.category.products.remove(instance)

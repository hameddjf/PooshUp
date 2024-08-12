from django import template
from connect.views import CreatorView

register = template.Library()


@register.filter
def get_related_categories(product, related_categories):
    """دسته‌های مرتبط با محصول را برمی‌گرداند."""
    return related_categories.get(product.id, [])


@register.filter
def get_profile_image(user):
    view = CreatorView()
    return view.get_profile_image(user)

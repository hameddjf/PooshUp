import hashlib
from django.conf import settings
from django import template

from connect.views import CreatorView
from category.models import Category

register = template.Library()


@register.filter
def get_related_categories(product, categories):
    """
    Filter to get all categories related to a product.
    """
    related_categories = []
    current_category = product.category
    while current_category:
        related_categories.append(current_category)
        current_category = current_category.parent
    return related_categories


@register.filter
def get_profile_image(user):
    view = CreatorView()
    profile_image = view.get_profile_image(user)
    if profile_image:
        return profile_image
    elif user.email:
        return f"https://www.gravatar.com/avatar/{hashlib.md5(user.email.lower().encode()).hexdigest()}?d=identicon"
    else:
        return f"{settings.STATIC_URL}default_profile_image.png"


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)


@register.inclusion_tag('includes/paginate_by_dropdown.html')
def paginate_by_dropdown(current_paginate_by):
    """
    این تگ کاستوم برای ایجاد منوی انتخاب تعداد نمایش استفاده می‌شود.
    """
    options = [10, 20, 30]
    return {'current_paginate_by': current_paginate_by, 'options': options}

from django import template
from like.models import Like

register = template.Library()


@register.simple_tag(takes_context=True)
def display_like_info(context, product):
    request = context['request']
    device_id = context['view'].get_device_id(request)

    try:
        like = Like.objects.get(product=product, device_info=device_id)
        liked = True
    except Like.DoesNotExist:
        liked = False

    like_count = product.likes.count()

    return {
        'liked': liked,
        'like_count': like_count,
        'product': product
    }

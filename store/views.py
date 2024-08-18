from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Min, Max, IntegerField
from django.db.models.functions import Cast
from django.contrib import messages
from .models import Product, ReviewRating, ProductGallery, Variation
from .forms import ReviewForm

from category.models import Category
from carts.models import Cart, CartItem
from orders.models import OrderProduct
from carts.views import _cart_id
# Create your views here.

from django.views.generic import ListView
from django.db.models import Min, Max
from .models import Product, Category, Variation


class StoreView(ListView):
    model = Product
    template_name = 'store/store.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_paginate_by(self, queryset):
        page_size = self.request.GET.get('page_size', 8)
        try:
            page_size = int(page_size)
        except ValueError:
            page_size = 8
        return page_size

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_available=True)

        active_variations = Variation.objects.filter(is_active=True)
        self.all_variations = active_variations

        # مرتب‌سازی
        sort_option = self.request.GET.get('sort')
        if sort_option == 'latest':
            queryset = queryset.order_by('-created_date')
        elif sort_option == 'min_price':
            queryset = queryset.order_by('price')
        elif sort_option == 'max_price':
            queryset = queryset.order_by('-price')
        elif sort_option == 'most_discount':
            queryset = queryset.order_by('-discount')

        # Category filter
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            main_category = Category.objects.get(slug=category_slug)
            related_categories = main_category.get_all_subcategories()
            all_category_ids = [cat.id for cat in related_categories]
            queryset = queryset.filter(category__id__in=all_category_ids)

        # Implement price range filter
        products_with_prices = queryset.exclude(price__isnull=True)
        min_price = products_with_prices.aggregate(
            min_price=Min('price'))['min_price'] or 0
        max_price = products_with_prices.aggregate(
            max_price=Max('price'))['max_price'] or 0

        self.min_price = min_price
        self.max_price = max_price

        price_ranges = []
        price_step = 45000
        current_min = min_price
        current_max = min_price + price_step

        while current_max <= max_price:
            price_range = f'${current_min:.0f} - ${current_max:.0f}'
            products_in_range = products_with_prices.filter(
                price__gte=current_min, price__lt=current_max)
            product_count = products_in_range.count()
            price_ranges.append((price_range, product_count))
            current_min += price_step
            current_max += price_step

        self.price_ranges = price_ranges

        # Size filter
        selected_sizes = self.request.GET.getlist('size')
        if selected_sizes:
            queryset = queryset.filter(
                variation__variation_value__in=selected_sizes, variation__variation_category='size')

        # Color filter
        selected_colors = self.request.GET.getlist('color')
        if selected_colors:
            queryset = queryset.filter(
                variation__variation_value__in=selected_colors, variation__variation_category='color')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['product_count'] = self.get_queryset().count()

        # همه رنگ‌ها
        selected_colors = self.request.GET.getlist('color')
        all_colors = Variation.objects.filter(variation_category='color', is_active=True).values_list(
            'variation_value', flat=True).distinct()
        context['all_colors'] = all_colors
        context['selected_colors'] = selected_colors
        context['color_product_counts'] = {color: queryset.filter(
            variation__variation_value=color, variation__variation_category='color').count() for color in all_colors}

        # همه اندازه‌ها
        selected_sizes = self.request.GET.getlist('size')
        all_sizes = Variation.objects.filter(variation_category='size', is_active=True).values_list(
            'variation_value', flat=True).distinct()
        context['all_sizes'] = all_sizes
        context['selected_sizes'] = selected_sizes
        context['size_product_counts'] = {size: queryset.filter(
            variation__variation_value=size, variation__variation_category='size').count() for size in all_sizes}

        # شمارش محصولات برای هر رنگ و اندازه
        color_product_counts = {color: self.get_queryset().filter(
            variation__variation_value=color, variation__variation_category='color').count() for color in all_colors}
        context['color_product_counts'] = color_product_counts

        size_product_counts = {size: self.get_queryset().filter(
            variation__variation_value=size, variation__variation_category='size').count() for size in all_sizes}
        context['size_product_counts'] = size_product_counts

        context['all_colors'] = Variation.objects.filter(
            variation_category='color', is_active=True).values_list('variation_value', flat=True).distinct()
        context['all_sizes'] = Variation.objects.filter(
            variation_category='size', is_active=True).values_list('variation_value', flat=True).distinct()
        context['color_product_counts'] = {color: self.get_queryset().filter(
            variation__variation_value=color, variation__variation_category='color').count() for color in context['all_colors']}
        context['size_product_counts'] = {size: self.get_queryset().filter(
            variation__variation_value=size, variation__variation_category='size').count() for size in context['all_sizes']}
        context['price_ranges'] = self.price_ranges
        context['selected_price_range'] = self.request.GET.getlist('price')
        context['sort'] = self.request.GET.get('sort')
        context['page_size'] = self.get_paginate_by(self.get_queryset())
        return context

# def store(request, category_slug=None):
#     categories = None
#     products = None

#     # Category filter
#     if category_slug is not None:
#         main_category = get_object_or_404(Category, slug=category_slug)
#         related_categories = main_category.get_all_subcategories()
#         all_category_ids = [cat.id for cat in related_categories]
#         products = Product.objects.filter(
#             category__id__in=all_category_ids, is_available=True).order_by('id')
#     else:
#         products = Product.objects.all().filter(
#             is_available=True).order_by('id')

#     # Implement price range filter
#     products_with_prices = products.exclude(price__isnull=True)
#     min_price = products_with_prices.aggregate(
#         min_price=Min('price'))['min_price'] or 0
#     max_price = products_with_prices.aggregate(
#         max_price=Max('price'))['max_price'] or 0

#     price_ranges = []
#     price_step = 30000
#     current_min = min_price
#     current_max = min_price + price_step

#     while current_max <= max_price:
#         price_range = f'${current_min:.0f} - ${current_max:.0f}'
#         products_in_range = products_with_prices.filter(
#             price__gte=current_min, price__lt=current_max)
#         product_count = products_in_range.count()
#         price_ranges.append((price_range, product_count))
#         current_min += price_step
#         current_max += price_step

#     selected_price_range = request.GET.getlist('price')

#     if selected_price_range:
#         for price_range in selected_price_range:
#             min_price, max_price = map(float, price_range.split(' - '))
#             products = products.filter(
#                 price__gte=min_price, price__lt=max_price)
#     else:
#         products = products

#     # Color filter
#     selected_colors = request.GET.getlist('color')
#     if selected_colors:
#         color_variations = Variation.objects.filter(
#             variation_category='color', variation_value__in=selected_colors, is_active=True)
#         product_ids = [v.product.id for v in color_variations]
#         products = products.filter(id__in=product_ids)

#     # Size filter
#     selected_sizes = request.GET.getlist('size')
#     if selected_sizes:
#         size_variations = Variation.objects.filter(
#             variation_category='size', variation_value__in=selected_sizes, is_active=True)
#         product_ids = [v.product.id for v in size_variations]
#         products = products.filter(id__in=product_ids)

#     # Paginator
#     paginator = Paginator(products, 8)
#     page = request.GET.get('page')
#     paged_products = paginator.get_page(page)

#     # Get all available colors and sizes
#     all_colors = Variation.objects.filter(
#         variation_category='color', is_active=True).values_list('variation_value', flat=True).distinct()
#     all_sizes = Variation.objects.filter(
#         variation_category='size', is_active=True).values_list('variation_value', flat=True).distinct()

#     # Count products for each color and size
#     color_product_counts = {color: products.filter(
#         variation__variation_value=color, variation__variation_category='color').count() for color in all_colors}
#     size_product_counts = {size: products.filter(
#         variation__variation_value=size, variation__variation_category='size').count() for size in all_sizes}

#     product_count = products.count()

#     context = {
#         'products': paged_products,
#         'product_count': product_count,
#         'categories': categories,
#         'all_colors': all_colors,
#         'all_sizes': all_sizes,
#         'color_product_counts': color_product_counts,
#         'size_product_counts': size_product_counts,
#         'price_ranges': price_ranges,
#         'selected_price_range': selected_price_range,
#     }
#     return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        cart = Cart.objects.get(cart_id=_cart_id(request=request))
        in_cart = CartItem.objects.filter(
            cart=cart,
            product=single_product
        ).exists()
    except Exception:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(
                user=request.user, product_id=single_product.id).exists()
        except Exception:
            orderproduct = None
    else:
        orderproduct = None

    reviews = ReviewRating.objects.filter(
        product_id=single_product.id, status=True)

    # Get the product gallery
    product_gallery = ProductGallery.objects.filter(
        Product_id=single_product.id)

    context = {
        'single_product': single_product,
        'in_cart': in_cart if 'in_cart' in locals() else False,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }
    return render(request, 'store/product_detail.html', context=context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by(
                '-created_date').filter(
                    Q(description__icontains=keyword) | Q(
                        title__icontains=keyword)
            )
            product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            review = ReviewRating.objects.get(
                user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=review)
            form.save()
            messages.success(
                request, "متشکرم! بررسی شما به روز شده است.")
            return redirect(url)
        except Exception:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(
                    request, "متشکرم! بررسی شما ارسال شده است.")
                return redirect(url)

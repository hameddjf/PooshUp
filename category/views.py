from store.models import Product, ReviewRating

from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView
from django.db.models import Avg, Count, Min, Max, Q

from .models import Category
# Create your views here.


class BaseView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('paginate_by', self.paginate_by)
        if paginate_by in [12, 24, 36]:
            return int(paginate_by)
        return self.paginate_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort')

        # دسته‌بندی‌های دارای حداقل یک محصول موجود
        available_categories = Category.objects.filter(
            product__stock__gt=0
        ).annotate(
            product_count=Count('product')
        ).order_by('-product_count')[:12]
        context['available_categories'] = available_categories

        # فیلتر کردن محصولات
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        in_stock = self.request.GET.get('in_stock') == 'true'
        category_id = self.request.GET.get('category')

        def get_related_categories(category):
            """تابعی برای گرفتن تمام دسته‌بندی‌های مرتبط به یک دسته."""
            related_categories = [category]
            if category.parent:
                related_categories += get_related_categories(category.parent)
            return related_categories

        context['categories'] = Category.objects.filter(parent__isnull=True)

        if category_id:
            # گرفته شدن دسته بندی اصلی
            main_category = get_object_or_404(Category, id=category_id)

            # استفاده از تابع برای گرفتن همه دسته‌های مرتبط
            related_categories = get_related_categories(main_category)

            # جمع‌آوری IDهای دسته‌ها و زیرشاخه‌ها
            all_category_ids = [cat.id for cat in related_categories] + \
                list(main_category.subcategories.values_list('id', flat=True))

            # گرفتن محصولات از دسته بندی اصلی و زیرشاخه‌ها
            context['products'] = Product.objects.filter(
                category__id__in=all_category_ids)
        else:
            context['products'] = Product.objects.all()

        queryset = context['products']
        if min_price and max_price:
            queryset = queryset.filter(
                price__gte=min_price, price__lte=max_price)
        if in_stock:
            queryset = queryset.filter(stock__gt=0)

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

        context['products'] = queryset  # به روز رسانی محصولات در کانتکست

        # قیمت‌های حداقل و حداکثر
        context['min_price'] = Product.objects.aggregate(Min('price'))[
            'price__min'] or 0
        context['max_price'] = Product.objects.aggregate(Max('price'))[
            'price__max'] or 0
        # بیشترین تخفیف
        context['most_discount'] = Product.objects.order_by(
            '-discount').first()
        # موجود
        context['available_products'] = Product.objects.filter(
            stock__gt=0).count()
        context['related_categories'] = {product.id: get_related_categories(
            product.category) for product in context['products']}

        # دسته‌بندی‌های زیر دسته
        context['subcategories'] = Category.objects.filter(
            parent__isnull=False)

        # صفحه بندی
        context['paginate_by'] = self.get_paginate_by(self.object_list)

        # شمارش تعداد محصولات هر دسته‌بندی
        for category in context['subcategories']:
            category.product_count = Product.objects.filter(
                category=category).count()

        # شمارش تعداد محصولات هر دسته‌بندی
        for category in context['categories']:
            category.product_count = Product.objects.filter(
                category=category).count()

        return context

# class BaseView(TemplateView):
#     template_name = 'index.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         # Get all products
#         products = Product.objects.filter(
#             is_available=True).order_by('created_date')

#         # Get reviews
#         reviews = ReviewRating.objects.filter(status=True)

#         # Get main categories
#         main_categories = Category.objects.filter(parent=None)

#         # Define the filters
#         filters = {
#             'قیمت': {
#                 'بالاترین قیمت': lambda p: p.order_by('-price'),
#                 'پایین‌ترین قیمت': lambda p: p.order_by('price'),
#                 'بالاترین تخفیف': lambda p: p.filter(discount__gt=0).order_by('-discount'),
#                 'کمترین تخفیف': lambda p: p.filter(discount__gt=0).order_by('discount'),
#             },
#             'موجودی': {
#                 'موجود': lambda p: p.filter(stock__gt=0),
#                 'ناموجود': lambda p: p.filter(stock=0),
#             },
#             'جدیدترین': lambda p: p.order_by('-created_date'),
#         }

#         # Get the selected filter from the request
#         selected_filter = self.request.GET.get('filter', 'جدیدترین')

#         # Apply the selected filter
#         if selected_filter in filters:
#             products = filters[selected_filter](products)

#         context.update({
#             'products': products,
#             'reviews': reviews,
#             'main_categories': main_categories,
#             'filters': filters,
#             'selected_filter': selected_filter,
#         })
#         return context

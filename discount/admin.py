from django.contrib import admin
from django.utils.html import format_html
from .models import Discount
from category.models import Category


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_percentage', 'start_date',
                    'end_date', 'is_active', 'products_display', 'category', )
    list_filter = ('is_active', 'start_date', 'end_date', 'category', )
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('products',)

    def products_display(self, obj):
        product_links = []
        for product in obj.products.all():
            product_links.append(f'<a href="{product.get_admin_url()}" target="_blank">{product.name}</a>')
        return format_html(', '.join(product_links))
    products_display.short_description = 'محصولات'
    products_display.allow_tags = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('products', 'category', )

    def save_model(self, request, obj, form, change):
        obj.save()
        obj.products.set(form.cleaned_data['products'])

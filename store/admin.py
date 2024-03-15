from django.contrib import admin
from .models import Product, Variation
# Register your models here.

# @admin.register()


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'price', 'stock',
                    'category', 'created_date', 'is_available')
    prepopulated_fields = {'slug': ('title',)}


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category',
                    'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category',
                   'variation_value')


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
